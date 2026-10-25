@fieldwise_init
struct _ObjType(Copyable, Movable):
    def BEGIN(self, a: Int):
        pass
def main():
    var obj = _ObjType()
    obj.BEGIN(42)
