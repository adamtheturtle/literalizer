@fieldwise_init
struct _ThingType(Copyable, Movable):
    def go[*Ts: Movable](self, var *args: *Ts) -> None:
        pass
def main():
    var thing = _ThingType()
    thing.go(List[String](), List([1]), List[String]())
    thing.go(List(["text"]), List([2]), List[String]())
    thing.go(List[String](), List(["text"]), List[String]())
    thing.go(List(["text"]), List([2]), List([3]))
