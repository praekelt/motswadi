from motswadi.workers import USSDApplicationWorker
from vumi.application.tests.test_base import ApplicationTestCase


class USSDApplicationWorkerTestCase(ApplicationTestCase):
    application_class = USSDApplicationWorker

    def setUp(self):
        super(USSDApplicationWorkerTestCase, self).setUp()
        self.app = self.get_application({}).result

    def test_consume_user_message(self):
        pass
