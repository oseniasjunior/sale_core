from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_channel_message(group_name: str, content: dict) -> None:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, {
        "type": "group.message",
        "content": content
    })
