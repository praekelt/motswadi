from vumi.application.base import ApplicationWorker


class USSDApplicationWorker(ApplicationWorker):
    """
    Main Motswadi application worker responsible for
    menu navigation and info replies. 
    """
    def consume_user_message(self, message):
        """
        Process incomming messages, return next menu item
        or requested information.
        """
        self.reply_to(message, "Dummy reply.")
