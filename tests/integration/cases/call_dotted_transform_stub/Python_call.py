def process(*_args: object, **_kwargs: object) -> object: ...
class _TracerType:
    def emit(self, *_args: object, **_kwargs: object) -> object: ...
tracer = _TracerType()
tracer.emit(process(value="hello"))
tracer.emit(process(value=42))
tracer.emit(process(value=True))
