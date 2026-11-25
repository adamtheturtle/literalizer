@fieldwise_init
struct _ThingType(Copyable, Movable):
    def go(self, var value: List[Int]) -> None:
        pass
def main():
    var thing = _ThingType()
    var my_data = thing.go(List([1]))
    _ = my_data
