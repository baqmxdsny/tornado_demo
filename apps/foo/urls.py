
from .handlers.foo import FooHandler, SleepHandler, SyncSleepHandler, NoSleepHandler, \
    ThreadSleepHandler, CelerySleepHandler, AsynchronousSleepHandler, DbSelect

url_patterns = [
    (r"/Too", FooHandler),
    (r"/Sleep", SleepHandler),
    (r"/Nosleep", NoSleepHandler),
    (r"/Threadsleep", ThreadSleepHandler),
    (r"/Syncsleep", SyncSleepHandler),
    (r"/Celerysleep", CelerySleepHandler),
    (r"/Asynchronoussleep", AsynchronousSleepHandler),
    (r"/DbSelect", DbSelect),

]
