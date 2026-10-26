@fieldwise_init
struct _ObjType(Copyable, Movable):
    def class(self, var a: Int):
        pass
def main():
    var obj = _ObjType()
    obj.class(42)
