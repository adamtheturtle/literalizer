class _HelperType:
    def list(self, *_args: object, **_kwargs: object) -> object: ...
helper = _HelperType()
helper.list(a=1)
