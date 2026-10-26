@fieldwise_init
struct _ThingType(Copyable, Movable):
    def Before(self, var value: Int):
        pass
def main():
    var thing = _ThingType()
    thing.Before(1)
