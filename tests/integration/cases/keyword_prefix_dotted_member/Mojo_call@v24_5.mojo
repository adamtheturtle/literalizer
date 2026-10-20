@fieldwise_init
struct _ThingType(Copyable, Movable):
    def first_value(self, value: Int):
        pass
def main():
    var thing = _ThingType()
    thing.first_value(1)
