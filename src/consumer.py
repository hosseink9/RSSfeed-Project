


def login_callback(chanel, method, properties, body):
    data = json.loads(body)
    user = User.objects.get(username=data['username'])
    notification_info = NotificationInfo.objects.create(message=data['message'])
    Notification.objects.create(user = user, message = notification_info)

