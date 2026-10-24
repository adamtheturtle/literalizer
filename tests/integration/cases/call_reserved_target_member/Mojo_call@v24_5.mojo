@fieldwise_init
struct _ObjType(Copyable, Movable):
    def class(self, a: Int):
        pass
def main():
    var obj = _ObjType()
    obj.class(42)
