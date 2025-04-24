
from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'store_id', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['created_at', 'updated_at']
        
    def create(self, validated_data):
        return Conversation.objects.create(**validated_data)