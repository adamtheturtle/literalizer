@fieldwise_init
struct _ObjType(Copyable, Movable):
    def ZKV(self, value: Int):
        pass
def main():
    var obj = _ObjType()
    obj.ZKV(1)
