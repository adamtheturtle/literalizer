class _ObjType:
    def ZVal(self, *_args: object, **_kwargs: object) -> object: ...
obj = _ObjType()
my_data = obj.ZVal(_arg=42) // note
