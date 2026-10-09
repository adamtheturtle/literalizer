@fieldwise_init
struct _ThingType(Copyable, Movable):
    def go[*Ts: AnyType](self, *args: *Ts) -> None:
        pass
def main():
    var thing = _ThingType()
    var my_data = thing.go(List[String]())
    _ = my_data
