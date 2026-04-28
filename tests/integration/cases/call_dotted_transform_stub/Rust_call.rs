fn main() {
    fn process<A>(_value: A) {}
    struct LogType_;
    impl LogType_ { fn emit<A>(&self, __arg: A) {} }
    let log = LogType_;
    log.emit(process("hello"));
    log.emit(process(42));
    log.emit(process(true));
}
