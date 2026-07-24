fn main() {
    fn process<A>(_value: A) {}
    fn emit<A, B>(__call: A, __zip: B) {}
    emit(process("hello"), "one");
    emit(process(42), "zero");
}
