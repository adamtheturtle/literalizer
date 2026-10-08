@fieldwise_init
struct _ThingType(Copyable, Movable):
    def go(self) -> None:
        pass
def main():
    var thing = _ThingType()
    thing.go()
