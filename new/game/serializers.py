from game.models import partie
from .models import Account
from rest_framework import serializers
from myaccount.serializers import AccountSerializer

class GameSerializer(serializers.ModelSerializer):
    player1 = AccountSerializer()
    player2 = AccountSerializer()

    class Meta:
        model = partie
        fields = ('id', 'player1', 'player2', 'score_player1', 'score_player2', 'time')


    """
    def get_messages(self, obj):
        messages = obj.messages.all()
        return PrivateMessageSerializer(messages, many=True).data
    """