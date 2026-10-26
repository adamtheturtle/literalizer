@fieldwise_init
struct _ThingType(Copyable, Movable):
    def go[*Ts: Movable](self, var *args: *Ts) -> None:
        pass
def main():
    var thing = _ThingType()
    var my_data = thing.go(List[String]())
    _ = my_data
