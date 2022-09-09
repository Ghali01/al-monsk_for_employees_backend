from channels.generic.websocket import WebsocketConsumer
from .models import AttendRecord

class AttendConsumer(WebsocketConsumer):

    def connect(self):
        # print('connect')
        if self.scope['user'].is_anonymous:
            self.close()
            return
        # if not self.scope['user'].online:
        self.scope['user'].online=True
        self.scope['user'].save()
        AttendRecord.objects.create(employee=self.scope['user'].employee,type=True)
        self.accept()


    def disconnect(self, code):
        # print('disconnect')

        self.scope['user'].online=False
        self.scope['user'].save()
        AttendRecord.objects.create(employee=self.scope['user'].employee,type=False)
