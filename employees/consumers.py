import asyncio
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer,async_to_sync
from .models import AttendRecord
from django.core.cache import cache
from json import dumps

class AttendConsumer(WebsocketConsumer):

    def connect(self):
        # print('connect')
        if self.scope['user'].is_anonymous:
            self.close()
            return
        # if not self.scope['user'].online:
       
        if self.connectionsCount()==0:
            self.scope['user'].online=True
            self.scope['user'].save()
            AttendRecord.objects.create(employee=self.scope['user'].employee,type=True)
            self.sendToStaff(True)

       
        self.accept()
        self.changeConnectionsCount(1)
    def disconnect(self, code):
        # print('disconnect')

        if self.connectionsCount()==1:
            self.scope['user'].online=False
            self.scope['user'].save()
            AttendRecord.objects.create(employee=self.scope['user'].employee,type=False)
            self.sendToStaff(False)
        self.changeConnectionsCount(-1)
    def connectionsCount(self):
        
        key='connections-'+str(self.scope['user'].id)
        count=cache.get(key,0)       
        return count
    def changeConnectionsCount(self,delta):
        
        key='connections-'+str(self.scope['user'].id)
        count=cache.get(key,0)        
        count+=delta
        cache.set(key,count)
        return count
   
    @async_to_sync
    async def sendToStaff(self,op):
        await self.channel_layer.group_send('staff',{
            'type':'noti.send',
            'firstName':self.scope['user'].firstName,
            'secondName':self.scope['user'].secondName,
            'id':self.scope['user'].employee.id, 
            'op':op
        })


class StaffConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('staff',self.channel_name)

    async def noti_send(self,event):
       
        msg=dumps(event)
        print(msg)
        await self.send(msg)

    async def disconnect(self, code):
        await self.channel_layer.group_discard('staff',self.channel_name)