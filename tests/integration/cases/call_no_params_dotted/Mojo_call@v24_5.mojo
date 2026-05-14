@fieldwise_init
struct _ThrottlerType(Copyable, Movable):
    def check(self):
        pass
def main():
    var throttler = _ThrottlerType()
    throttler.check()
    throttler.check()
