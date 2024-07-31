import json
import time
import asyncio
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ball, pad, partie 
from .globals import setGame, getGame, removeGame, setCups, getCup, removeCup
from .pongGame import pongGame, matchmaking
from channels.db import database_sync_to_async
from .tournament import tournament

queue = []
nb_room = 0
connected_users = {}
matchmaking_task = None
class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.user = self.scope['user']
        if isinstance(self.user, AnonymousUser):
            await self.close()
        
        self.room_name = None
        self.room = None
        self.cup_name = None
        self.room_group_name = None
        self.player_side = None
        self.in_lobby = False
        self.in_cup = False
        self.in_game = False
        if self.user in connected_users:
            await self.close()
        else :
            connected_users[self.user.id] = self
        await self.save_user(self.user)
        await self.accept()
        print(connected_users)

    async def disconnect(self, close_code):

        global matchmaking_task
        if self.in_cup != False:
            if self.cup.state == 0:
                await self.cup.leavingPlayer(self.user, self)
            if self.cup.state > 0:
                if self.room.left_player == self.user:
                    self.room.score[1] = 5
                    self.room.game_over = True
                elif self.room.right_player == self.user:
                    self.room.score[0] = 5
                    self.room.game_over = True
            self.cup = None
            self.cup_group_name = None
            self.in_cup = False
            self.room = None
            self.room_name = None
            self.player_side = None
            self.in_lobby = False
        if self.room_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            if self.room:
                if self.player_side == 'left' and self.room.right_player == None: #CHECK A DROITE YA QUELQUUN 
                    self.room.left_player = None
                elif self.player_side == 'right' and self.room.left_player == None:
                    self.room.right_player = None
                elif self.player_side == 'left' and self.room.right_player != None : #CHECK A DROITE YA QUELQUUN 
                    self.room.test = True
                    self.room.dc_side = 'left'
                elif self.player_side == 'right' and self.room.left_player != None :
                    self.room.test = True
                    self.room.dc_side = 'right'
                if not self.room.left_player and not self.room.right_player:
                    removeGame(self.room_name)
                else:
                    await self.save_user(self.room.left_player)
                    await self.save_user(self.room.right_player)
            
            if self.user in connected_users:
                print(f'Deleting connected player {connected_users[self.user.id]} ...')
                del connected_users[self.user.id]
        
        for player in queue:
            if self == player:
                queue.remove(self)
        
        if not queue and matchmaking_task and not matchmaking_task.done():
            matchmaking_task.cancel()
            matchmaking_task = None

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        action = data.get('action')
        print(action)
        if action == 'join':
            mode = data.get('mode')
            room_name = data.get('room')
            
            print(mode)
            print(room_name)
            if mode == 'pvp':
                self.in_lobby = False
                if room_name == "matchmaking":
                    global nb_room
                    global matchmaking_task
                    nb_room += 1
                    await self.add_player_to_queue()
                    if matchmaking_task is None or matchmaking_task.done():
                        matchmaking_task = asyncio.create_task(matchmaking(queue))
                elif room_name[:4] != "room" and room_name != "cup":
                    self.room_name = room_name.replace(" ", "")
                    if int(self.room_name.split("-")[0]) != self.user.id and int(self.room_name.split("-")[1]) != self.user.id:
                        print("Invalid room name")
                        return
                    self.room = getGame(self.room_name)
                    self.room_group_name = f"game_{self.room_name}"
                    
                    if self.room is None:
                        await self.create_room()
                    else:
                        await self.join_existing_room()
                elif room_name == "cup":
                    i = 0
                    while not self.in_cup:
                        self.cup_name = f"{i}cup"
                        self.cup = getCup(self.cup_name)
                        self.cup_group_name = f"game_{self.cup_name}"
                        if self.cup is None:
                            await self.create_cup(i)
                        else:
                            if self.cup.player_count < 8:
                                await self.join_existing_cup()
                        i += 1
                else:
                    print("Invalid room name")
                    
            elif mode == 'ai':
                await self.setup_ai_game(data.get('room'))
                
        elif action == 'move' and self.room and not self.room.game_over:
            if self.room.game_state:
                direction = data.get('direction')
                if self.player_side == 'left':
                    self.room.leftPad.direction = direction
                elif self.player_side == 'right':
                    self.room.rightPad.direction = direction

        elif action == 'leave_queue':
            player_id = data.get('player_id')
            await self.leave_queue()

        elif action == 'leave_cup':
            if self.in_cup == True:
                print("YO") 
                await self.cup.leavingPlayer(self.user, self) 
                self.cup = None
                self.cup_group_name = None
            self.in_cup = False

        elif action == 'status':
            await self.send(text_data=json.dumps({
                'type': 'status',
                'in_lobby': self.in_lobby,
                'in_cup': self.in_cup,
                'matches' : self.cup.all_rounds if self.in_cup != False else None
            }))
            if self.in_lobby and self.room:
                await self.send(text_data=json.dumps({
                    'type': 'game_info',
                    'left': self.room.left_player.id if self.room.left_player else None,
                    'right': self.room.right_player.id if self.room.right_player else None,
                }))

    async def lost_cup(self):        
        self.cup_group_name = None
        self.room_name = None
        self.cup = None
        self.player_side = None
        self.in_lobby = False
        self.room_group_name = None
        self.in_cup = False

    async def leave_queue(self):

        global matchmaking_task
        if self in queue:
            queue.remove(self)
            await self.send(text_data=json.dumps({
                'action': 'left_queue',
            }))
            print(f"{self} removed from queue")
            if not queue and matchmaking_task and not matchmaking_task.done():
                matchmaking_task.cancel()
                matchmaking_task = None

    async def game_info(self, event):
        game_info = event['game_info']
        await self.send(text_data=json.dumps(game_info))

    async def lobby_state(self, event):
        lobby_state = event['lobby_state']
        await self.send(text_data=json.dumps(lobby_state))

    async def cup_match_result(self, event):
        cup_match_result = event['cup_match_result']
        await self.send(text_data=json.dumps(cup_match_result))

    async def game_state(self, event):
        game_state = event['game_state']
        await self.send(text_data=json.dumps(game_state))
        
    async def tournament_state(self, event):
        tournament_state = event['tournament_state']
        await self.send(text_data=json.dumps(tournament_state))

    async def next_match(self, event):
        next_match = event['next_match']
        await self.send(text_data=json.dumps(next_match))

    async def countdown(self, event):
        countdown = event['countdown']
        await self.send(text_data=json.dumps({'type': 'countdown', 'countdown': countdown}))

    async def game_result(self, event):
        game_result = event['game_result']
        await self.send(text_data=json.dumps({'type': 'game_result', 'game_result': game_result}))

    async def create_room(self):
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.player_side = 'left'
        self.room = pongGame(self.room_name, self)
        setGame(self.room_name, self.room)
        self.room.left_player = self.user
        self.in_lobby = True
        
    async def create_cup(self, i=None):
        await self.channel_layer.group_add(
            self.cup_group_name,
            self.channel_name
        )
        self.cup = tournament(self.user, self, self.cup_name)
        setCups(self.cup_name, self.cup)
        self.in_cup = True

    async def join_existing_cup(self):
        await self.channel_layer.group_add(
            self.cup_group_name,
            self.channel_name
        )
        await self.cup.newContestant(self.user, self)
        self.in_cup = True
    
    async def join_existing_room(self):
        if self.room.player_number == 1:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            self.player_side = 'right'
            self.room.right_player = self.user
            await self.room.launchGame("Online", 0, False)
            self.in_lobby = True

    async def setup_ai_game(self, diff):
        self.diff = diff
        self.room_name = "ai"
        i = 0
        while getGame(self.room_name) is not None:
            self.room_name = f"{i}ai"
            i += 1
        self.room_group_name = f"game_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.player_side = 'left'
        self.room = pongGame(self.room_name, self)
        setGame(self.room_name, self.room)
        self.room.left_player = self.user
        await self.room.launchGame("LM", self.diff, False)
    
    async def add_player_to_queue(self):
        
        print('Adding player to queue...')
        self.wait_time = time.time()
        queue.append(self)
        print(f'player : {self.user}')
        print(f'Is player authenticated : {self.user.is_authenticated}')
        print(f'player\'s id : {self.user.id if self.user else "No ID"}')
        print(f'player\'s username : {self.user.username if self.user else "No user"}')
        print(f'player\'s elo : {self.user.elo if self.user else "No elo"}')
        
        await self.send(text_data=json.dumps({
            'action': 'joined_queue',
            'user_id': self.user.id
        }))

    async def start_match(self):
        
        global nb_room
        print('Starting match...')

        self.room_name = f"{nb_room}room"
        self.room = getGame(f"{nb_room}room")
        self.room_group_name = f"game_{self.room_name}"
        
        if self.room is None :
            print('player1 creating room...')
            await self.create_room()
        else:
            print('player2 joining room...')
            await self.join_existing_room()
    
    @database_sync_to_async
    def save_user(self, user):
        user.save()

def get_user_instance(user_id):   
    return connected_users.get(user_id)
