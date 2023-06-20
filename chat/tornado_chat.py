# import tornado.web
# import tornado.websocket
# import tornado.ioloop
# print('hello')
# class ChatHandler(tornado.websocket.WebSocketHandler):
#     active_connections = set()

#     def open(self):
#         self.active_connections.add(self)

#     def on_message(self, message):
        # for conn in self.active_connections:
        #     conn.write_message(message)

#     def on_close(self):
#         self.active_connections.remove(self)

# def make_app():
#     return tornado.web.Application([
#         (r"/chat", ChatHandler),
#     ])

# if __name__ == "__main__":
#     app = make_app()
#     app.listen(8888)
#     tornado.ioloop.IOLoop.current().start()



# import tornado.escape
# import tornado.ioloop
# import tornado.web
# import tornado.websocket


# class User:
#     def __init__(self, username):
#         self.username = username
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket


class User:
    def __init__(self, username):
        self.username = username


class ChatHandler(tornado.websocket.WebSocketHandler):
    users = []

    def initialize(self, username):
        self.user = User(username)
        self.users.append(self.user)
        self.send_user_list()

    def open(self):
        pass

    def on_close(self):
        self.users.remove(self.user)
        self.send_user_list()

    def on_message(self, message):
        for conn in self.active_connections:
            conn.write_message(message)
        # Handle chat message logic here

    def send_user_list(self):
        user_list = [user.username for user in self.users]
        self.write_message({"user_list": user_list})


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("app/login.html")

    def post(self):
        username = self.get_argument("username")
        self.redirect(f"/chat?user={username}")


class ChatPageHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument("user", None)
        if username:
            self.render("app/chat.html", username=username)
        else:
            self.redirect("/login")


def make_app():
    return tornado.web.Application(
        [
            (r"/", ChatPageHandler),
            (r"/chat", ChatHandler),
            (r"/login", LoginHandler),
        ],
        cookie_secret="YOUR_COOKIE_SECRET",
        static_path="static",
        template_path="templates",
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
