@fieldwise_init
struct _HelperType(Copyable, Movable):
    def list(self, a: Int):
        pass
def main():
    var helper = _HelperType()
    helper.list(1)
