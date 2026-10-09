@fieldwise_init
struct _ThingType(Copyable, Movable):
    def go[*Ts: AnyType](self, *args: *Ts) -> None:
        pass
def main():
    var thing = _ThingType()
    var item = List([
        1,
        2,
    ])
    thing.go(item.copy())
