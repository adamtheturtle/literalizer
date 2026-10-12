@fieldwise_init
struct _ObjType(Copyable, Movable):
    def ZVal(self, _arg: Int) -> None:
        pass
def main():
    var obj = _ObjType()
    var my_data = obj.ZVal(42) // note
    _ = my_data
