@fieldwise_init
struct _ObjType(Copyable, Movable):
    def ZVal(self, var value: Int):
        pass
def main():
    var obj = _ObjType()
    obj.ZVal(1)
