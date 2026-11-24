from std.utils.variant import Variant
comptime Value = Variant[String, Int, List[Int], List[String]]
@fieldwise_init
struct _ThingType(Copyable, Movable):
    def go[*Ts: Movable](self, var *args: *Ts) -> None:
        pass
def main():
    var thing = _ThingType()
    thing.go(List[String](), List([Value(1)]), List[String]())
    thing.go(List([Value(String("text"))]), List([Value(2)]), List[String]())
    thing.go(List[String](), List([Value(String("text"))]), List[String]())
    thing.go(List([Value(String("text"))]), List([Value(2)]), List([Value(3)]))
