class QueueMember:

    def __init__(self, user_id: int, message_id: int):
        self.user_id = user_id
        self.message_id = message_id
        self.notifications_enabled = False
