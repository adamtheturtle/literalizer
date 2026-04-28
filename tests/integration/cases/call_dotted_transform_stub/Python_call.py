def process(*_args: object, **_kwargs: object) -> object: ...
class _LogType:
    def emit(self, *_args: object, **_kwargs: object) -> object: ...
log = _LogType()
log.emit(process(value="hello"))
log.emit(process(value=42))
log.emit(process(value=True))
