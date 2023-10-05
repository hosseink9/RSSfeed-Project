
def login_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    chanel = connection.channel()

    chanel.queue_declare(queue='login')
    chanel.basic_consume(queue='login', on_message_callback=login_callback)

    chanel.start_consuming()


