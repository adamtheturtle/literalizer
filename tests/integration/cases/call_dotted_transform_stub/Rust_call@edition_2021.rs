fn main() {
    fn process<A>(_value: A) {}
    struct TracerType;
    impl TracerType { fn emit<A>(&self, __arg: A) {} }
    let tracer = TracerType;
    tracer.emit(process("hello"));
    tracer.emit(process(42));
    tracer.emit(process(true));
}
