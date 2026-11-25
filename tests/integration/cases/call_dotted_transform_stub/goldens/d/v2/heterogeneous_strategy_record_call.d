void main() {
int process(T...)(T args) { return 0; }
struct TracerType_ { int emit(T...)(T args) { return 0; } }
TracerType_ tracer;
tracer.emit(process("hello"));
tracer.emit(process(42));
tracer.emit(process(true));
}
