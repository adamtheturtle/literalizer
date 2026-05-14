fn main() {
    fn process<A>(_value: A) {}
    struct TracerType_;
    impl TracerType_ { fn emit<A>(&self, __arg: A) {} }
    let tracer = TracerType_;
    tracer.emit(process("hello"));
    tracer.emit(process(42));
    tracer.emit(process(true));
}
