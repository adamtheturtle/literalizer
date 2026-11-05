def process(Map _args) { null }
class _TracerType { def emit(Map _args) { null } }
def tracer = new _TracerType()
tracer.emit(process(value: "hello"))
tracer.emit(process(value: 42))
tracer.emit(process(value: true))
