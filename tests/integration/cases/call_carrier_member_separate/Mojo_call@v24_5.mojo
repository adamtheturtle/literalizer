@fieldwise_init
struct _AppType(Copyable, Movable):
    def go(self, first_value: List[Int], second_value: List[String]):
        pass
def main():
    var app = _AppType()
    app.go(List([1]), List(["text"]))
