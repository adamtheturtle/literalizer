class _ObjType:
    def ZVal(self, *_args: object, **_kwargs: object) -> object: ...
obj = _ObjType()
obj.ZVal(value=1)
