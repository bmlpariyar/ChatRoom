from rest_framework.serializers import ModelSerializer
from base.models import Room, User, Topic



class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TopicSerializers(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']

class RoomSerializers(ModelSerializer):
    host = UserSerializers(read_only=True)
    topic = TopicSerializers(read_only=True)
    participants = UserSerializers(read_only=True, many=True)
    class Meta:
        model = Room
        fields = '__all__'