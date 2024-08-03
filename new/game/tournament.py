from .pongGame import pongGame
from .globals import setGame, getGame, removeGame, setCups, getCup, removeCup
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from myaccount.models import Account
from chat.consumers import chat_consumers
from chat.consumers import ChatConsumer

#class tournament_manager(AsyncWebsocketConsumer):
    #async def connect(self):
        #print("I EXIST \n")
        #await self.accept()
    
    #async def disconnect(self, close_code):
       #print("I DIED \n")

class tournament() :
    def __init__(self, user, pongConsumer, cup_name):
        self.max_players = 8
        self.cup_name = cup_name
        self.player_count = 1
        self.list_player = [(user, pongConsumer)]
        self.state = 0
        self.rooms = []
        self.tournament_consumer = pongConsumer
        self.cup_group_name = f'game_{self.cup_name}'
        self.rounds = []
        self.winners1 = []
        self.winners2 = []
        self.all_rounds = []
        print(self.list_player)

    async def newContestant(self, user, pongConsumer):
        self.player_count += 1 
        self.list_player.append((user, pongConsumer))
        await self.sendLobbyState()
        if self.player_count == self.max_players:
            await self.launchTournament()
        print(self.list_player)

    async def leavingPlayer(self, user, pongConsumer):
        i = 0
        to_remove = (user, pongConsumer)
        while (self.list_player[i] != to_remove and i < len(self.list_player)):
            i += 1
        self.player_count -= 1
        self.list_player.pop(i)
        pongConsumer.in_queue_cup = False
        if self.state == 0:
            await self.sendLobbyState()

    async def launchTournament(self) :
        self.state = 1
        seeding = [0, 7, 5, 2, 3, 4, 6, 1]
        self.list_player = sorted(self.list_player, key=lambda pair: pair[0].elo, reverse=True)
        bracket_list = [None] * len(self.list_player)
        for index, pos in enumerate(seeding):
            bracket_list[pos] = self.list_player[index]
        self.list_player = bracket_list
        for user, pongConsumer in self.list_player :
            pongConsumer.in_queue_cup = False
            pongConsumer.in_cup = True
        await self.save_is_in_game_all()
        await self.create_room_cup()

    async def send_chat_opponent(self, player1, player2):
        if player1.id in chat_consumers:
            await chat_consumers[player1.id].send(text_data=json.dumps(
                {
                    'message' : "Next tournament match against " + player2.username + " starts in 60 secs !",
                    'issuer': "Tournament Info",
                    'receiver' : player1.username
                }
            ))
        if player2.id in chat_consumers:
            await chat_consumers[player2.id].send(text_data=json.dumps(
                {
                    'message' : "Next tournament match against " + player2.username + " starts in 60 secs !",
                    'issuer': "Tournament Info",
                    'receiver' : player2.username
                }
            ))

    async def sendLobbyState(self):
        await self.tournament_consumer.channel_layer.group_send(
            self.cup_group_name,
            {
                'type': 'lobby_state',
                'lobby_state': {
                    'type': 'lobby_state',
                    'message': f"waiting for players: {self.player_count} / {self.max_players}" 
                }
            }
        )

    async def save_is_in_game_all(self):
        for user, pongConsumer in self.list_player :
            player = await database_sync_to_async(Account.objects.get)(id=user.id)
            player.is_in_game = True
            await database_sync_to_async(player.save)()
    
    async def save_tournament_place(self, loser):
        player = await database_sync_to_async(Account.objects.get)(id=loser.id)
        if self.state == 1:
            player.nb_top8 += 1
        elif self.state == 2:
            player.nb_top4 += 1
        elif self.state == 3: 
            player.nb_top2 += 1
        await database_sync_to_async(player.save)()

    async def save_winner_place(self, winner):
        player = await database_sync_to_async(Account.objects.get)(id=winner.id)
        player.nb_top1 += 1
        await database_sync_to_async(player.save)()
    async def save_is_not_in_game_winner(self, user) :
        player = await database_sync_to_async(Account.objects.get)(id=user.id)
        player.is_in_game = False
        await database_sync_to_async(player.save)()

    async def create_room_cup(self):
        i = 0
        matches = []
        while i < len(self.list_player) - 1:
            player1, consumer1 = self.list_player[i]
            player2, consumer2 = self.list_player[i + 1]
            room_name = f"cup_room{i}{self.cup_name}"
            room = pongGame(room_name, consumer1)
            setGame(room_name, room)
            self.set_room_player_side(room, player1, player2)
            room_cup_group_name = f"game_{room_name}"
            self.set_consumer_info(consumer1, consumer2, room, room_cup_group_name)
            await consumer1.channel_layer.group_add(
                room_cup_group_name,
                consumer1.channel_name
            )
            await consumer2.channel_layer.group_add(
            room_cup_group_name,
            consumer2.channel_name
            )
            self.rooms.append(room_name)
            await room.launchGame("Online", 0, True, consumer2) 
            match_info = {
                'player1': player1.username,
                'player2': player2.username,
                'room_name': room_name,
                'state': 'started'
            }
            matches.append(match_info)
            i += 2
            print(i)
            await self.send_chat_opponent(player1, player2)
        print(matches)
        
        await self.send_tournament_state(matches)

    async def discard_all_groups(self):
        channel_layer = get_channel_layer()
        for room_name in self.rooms:
            group_name = f"game_{room_name}"
            for user, pongConsumer in self.list_player:
                await pongConsumer.channel_layer.group_discard(
                    group_name,
                    pongConsumer.channel_name
                )
            removeGame(room_name)

    async def match_result(self, room_name, winner, loser):
        """
        await self.tournament_consumer.channel_layer.group_send(
            self.cup_group_name,
            {
                'type': 'cup_match_result',
                'cup_match_result': {
                    'type': 'cup_match_result',
                    'loser' : loser.id,
                    'loser_username' : loser.username,
                    'winner' : winner.id,
                    'winner_username' : winner.username,
                }
            }
        )
        """
        for user, pongConsumer in self.list_player:
            if user == loser:
                await pongConsumer.lost_cup()
                await self.save_tournament_place(loser)
        if self.state == 1 :
            for user, pongConsumer in self.list_player:
                if user == winner:
                    self.winners1.append((winner, pongConsumer))
                    break
            if len(self.winners1) > 3:
                await self.discard_all_groups()
                await self.create_room_cup_round_2()
        elif self.state == 2: 
            for user, pongConsumer in self.list_player:
                if user == winner:
                    self.winners2.append((winner, pongConsumer))
                    break
            if len(self.winners2) > 1:
                await self.discard_all_groups()
                await self.create_room_cup_round_3()
        elif self.state == 3:
            await self.tournament_consumer.channel_layer.group_send(
                self.cup_group_name,
                {
                    'type': 'lobby_state',
                    'lobby_state': {
                        'type': 'lobby_state',
                        'message': f"{winner.username} has won the tournament\n"
                    }
                }
            )
            for user, pongConsumer in self.list_player:
                if user == winner:
                    pongConsumer.in_cup = False
                    await pongConsumer.channel_layer.group_discard(
                        pongConsumer.cup_group_name,
                        pongConsumer.channel_name 
                    )
            await self.save_is_not_in_game_winner(winner)
            await self.save_winner_place(winner)
        del self

        
    async def create_room_cup_round_2(self):
        i = 0
        matches = []
        self.state = 2
        self.rooms = []
        while i < len(self.winners1) - 1:
            player1, consumer1 = self.winners1[i]
            player2, consumer2 = self.winners1[i + 1]
            room_name = f"cup_room{i}{self.cup_name}"
            room = pongGame(room_name, consumer1)
            setGame(room_name, room)
            self.set_room_player_side(room, player1, player2)
            room_cup_group_name = f"game_{room_name}"
            self.set_consumer_info(consumer1, consumer2, room, room_cup_group_name)
            await consumer1.channel_layer.group_add(
                room_cup_group_name,
                consumer1.channel_name
            )
            await consumer2.channel_layer.group_add(
            room_cup_group_name,
            consumer2.channel_name
            )
            self.rooms.append(room_name)
            await room.launchGame("Online", 0, True, consumer2) 
            match_info = {
                'player1': player1.username,
                'player2': player2.username,
                'room_name': room_name,
                'state': 'started'
            }
            matches.append(match_info)
            i += 2
        await self.send_tournament_state(matches)

    async def create_room_cup_round_3(self):
        i = 0
        matches = []
        self.state = 3
        self.rooms = []
        while i < len(self.winners2) - 1:
            player1, consumer1 = self.winners2[i]
            player2, consumer2 = self.winners2[i + 1]
            room_name = f"cup_room{i}{self.cup_name}"
            room = pongGame(room_name, consumer1)
            setGame(room_name, room)
            self.set_room_player_side(room, player1, player2)
            room_cup_group_name = f"game_{room_name}"
            self.set_consumer_info(consumer1, consumer2, room, room_cup_group_name)
            await consumer1.channel_layer.group_add(
                room_cup_group_name,
                consumer1.channel_name
            )
            await consumer2.channel_layer.group_add(
            room_cup_group_name,
            consumer2.channel_name
            )
            self.rooms.append(room_name)
            await room.launchGame("Online", 0, True, consumer2) 
            match_info = {
                'player1': player1.username,
                'player2': player2.username,
                'room_name': room_name,
                'state': 'started'
            }
            matches.append(match_info)
            i += 2
        await self.send_tournament_state(matches)



    async def lobby_state(self, event):
        lobby_state = event['lobby_state']
        await self.send(text_data=json.dumps(lobby_state))

    async def tournament_state(self, event):
        tournament_state = event['tournament_state']
        await self.send(text_date=json.dumps(tournament_state))

    async def send_tournament_state(self,  matches):
        print(matches)
        self.all_rounds.append(matches)
        await self.tournament_consumer.channel_layer.group_send(
            self.cup_group_name,
            {
                'type': 'tournament_state',
                'tournament_state': {
                    'type': 'tournament_state',
                    'state': self.state,
                    'matches': self.all_rounds
                }
            }
        )

    def set_consumer_info(self, consumer1, consumer2, room, room_cup_group_name) :
        room.tournament = self
        consumer1.room = room
        consumer2.room = room
        consumer1.player_side = "left"
        consumer2.player_side = "right"

    def set_room_player_side(self, room, P1, P2) :
        room.left_player = P1
        room.right_player = P2

    #async def tracking_result(self, winner)
