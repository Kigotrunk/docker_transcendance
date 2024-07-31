import time
import json
import asyncio
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from game.consumers import matchmaking, PongConsumer, queue

User = get_user_model()

class FakeUser:
    def __init__(self, user_id, username, elo):
        self.id = user_id
        self.username = username
        self.elo = elo
        self.is_authenticated = True

class FakeConsumer(PongConsumer):
    def __init__(self, user):
        self.user = user
        self.wait_time = time.time()

    async def send(self, text_data):
        print(f'Sending to {self.user.username}: {text_data}')

    async def start_match(self):
        print(f'Starting match for {self.user.username}')
        # Simulate some async match handling here
        await asyncio.sleep(1)

class Command(BaseCommand):
    help = 'Test the matchmaking function'

    def handle(self, *args, **kwargs):
        self.stdout.write('Testing matchmaking...')

        users = [
            FakeUser(1, 'Alice', 1200),
            FakeUser(2, 'Bob', 1250),
            FakeUser(3, 'Charlie', 1150),
            FakeUser(4, 'David', 1300),
        ]

        consumers = [FakeConsumer(user) for user in users]
        for consumer in consumers:
            queue.append(consumer)

        asyncio.run(matchmaking(queue))
        self.stdout.write('Matchmaking test completed.')