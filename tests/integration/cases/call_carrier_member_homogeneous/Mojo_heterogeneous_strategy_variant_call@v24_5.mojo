@fieldwise_init
struct _AppType(Copyable, Movable):
    def go(self, var first_value: List[Int], var second_value: List[Int]):
        pass
def main():
    var app = _AppType()
    app.go(List([1]), List([2]))
