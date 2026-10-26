fn main() {
    fn process<A>(_value: A) {}
    fn emit<A>(__arg: A) {}
    emit(process(42));
}
