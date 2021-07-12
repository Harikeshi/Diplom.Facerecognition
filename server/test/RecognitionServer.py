from server import Server


class RecognitionServer(Server):

    def handle(self, message):
        try:
            print("Got: {}".format(message))
        except Exception as e:
            print("Error: {}".format(e))


if __name__ == "__main__":
    print("RecognitionServer started.")

    app = RecognitionServer("localhost", 8889)
    app.start_server()
    app.loop()
    app.stop_server()