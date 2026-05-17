class Check {
static object process(object value = null) => null;
class TracerType_ { public object emit(object _arg = null) => null; }
static TracerType_ tracer = new TracerType_();
    public static void Main() {
tracer.emit(process("hello"));
tracer.emit(process(42));
tracer.emit(process(true));
    }
}
