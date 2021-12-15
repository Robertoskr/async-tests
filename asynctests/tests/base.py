from unittest import TestCase



class BaseTest(TestCase):
    maxDiff = None

    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)

    def setUp(self):
        #do something when the test start
        pass

    def tearDown(self):
        #do something when the test end
        pass

