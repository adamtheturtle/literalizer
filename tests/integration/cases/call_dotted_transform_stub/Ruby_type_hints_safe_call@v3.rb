def process(*a); end
class TracerType; def emit(*a, **kw); end; end
tracer = TracerType.new
tracer.emit(process(value: "hello"))
tracer.emit(process(value: 42))
tracer.emit(process(value: true))
