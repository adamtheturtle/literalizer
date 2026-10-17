from std.utils.variant import Variant
comptime Value = Variant[Int, String]
@fieldwise_init
struct _ClientType(Copyable, Movable):
    def go(self, first_value: List[Value], second_value: List[Value]):
        pass
@fieldwise_init
struct _AppType(Copyable, Movable):
    var client: _ClientType
def main():
    var app = _AppType(_ClientType())
    app.client.go(List([Value(1)]), List([Value(String("text"))]))
