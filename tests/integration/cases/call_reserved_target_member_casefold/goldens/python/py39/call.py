class _ObjType:
    def BEGIN(self, *_args: object, **_kwargs: object) -> object: ...
obj = _ObjType()
obj.BEGIN(a=42)
