from taskiq_nats import PullBasedJetStreamBroker

broker = PullBasedJetStreamBroker(servers="nats://127.0.0.1:4222", queue="taskiq_queue")
