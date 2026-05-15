class Main {
static Object process(Object... args) { return null; }
static class TracerType_ { Object emit(Object... args) { return null; } }
static TracerType_ tracer = new TracerType_();
    public static void main() {
tracer.emit(process("hello"));
tracer.emit(process(42));
tracer.emit(process(true));
    }
}
