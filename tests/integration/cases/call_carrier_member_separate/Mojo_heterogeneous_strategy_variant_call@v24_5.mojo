from std.utils.variant import Variant
comptime Value = Variant[Int, String]
@fieldwise_init
struct _AppType(Copyable, Movable):
    def go(self, first_value: List[Value], second_value: List[Value]):
        pass
def main():
    var app = _AppType()
    app.go(List([Value(1)]), List([Value(String("text"))]))
