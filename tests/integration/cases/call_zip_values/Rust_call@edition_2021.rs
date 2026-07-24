fn main() {
    fn process<A>(_value: A) {}
    fn emit<A, B>(__call: A, __zip: B) {}
    emit(process("hello"), 1);
    emit(process(42), 0);
}
