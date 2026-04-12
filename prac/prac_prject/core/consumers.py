import json
from  channels.generic.websocket import AsyncWebsocketConsumer

class OrderTrackingConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f"order_{self.order_id}"
        
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        
        await self.accept()
        
        async def location_update(self, event):
            
            latitude = event.get("latitude")
            longitude = event.get("longitude")
            
            await self.send(
                text_data = json.dumps({
                    "latitude": latitude,
                    "longitude": longitude,
                })
            )