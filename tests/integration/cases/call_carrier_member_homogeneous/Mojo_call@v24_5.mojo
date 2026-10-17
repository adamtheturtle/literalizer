@fieldwise_init
struct _AppType(Copyable, Movable):
    def go(self, first_value: List[Int], second_value: List[Int]):
        pass
def main():
    var app = _AppType()
    app.go(List([1]), List([2]))
