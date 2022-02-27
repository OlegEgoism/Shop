def callback(self, ch, method, properties, body):
    print("[django-rabbitmq] Received %r" % body)
