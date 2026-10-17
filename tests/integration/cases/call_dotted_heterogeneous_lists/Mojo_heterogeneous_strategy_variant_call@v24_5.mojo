from std.utils.variant import Variant
comptime Value = Variant[Int, String]
@fieldwise_init
struct _ClientType(Copyable, Movable):
    def go(self, first_value: List[Int], second_value: List[String]):
        pass
@fieldwise_init
struct _AppType(Copyable, Movable):
    var client: _ClientType
def main():
    var app = _AppType(_ClientType())
    app.client.go(List([Value(1)]), List([Value(String("text"))]))
