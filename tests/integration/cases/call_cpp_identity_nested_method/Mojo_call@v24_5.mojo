@fieldwise_init
struct _ThingType(Copyable, Movable):
    def go(self) -> None:
        pass
@fieldwise_init
struct _OuterType(Copyable, Movable):
    var thing: _ThingType
def main():
    var outer = _OuterType(_ThingType())
    outer.thing.go()
