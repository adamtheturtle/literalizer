object Fixture_call_dotted_transform_stub_Scala_call {
def process(value: Any = null): Any = null
class _TracerType { def emit(_arg: Any = null): Any = null }
val tracer = new _TracerType
tracer.emit(process(value = "hello"))
tracer.emit(process(value = 42))
tracer.emit(process(value = true))
}
