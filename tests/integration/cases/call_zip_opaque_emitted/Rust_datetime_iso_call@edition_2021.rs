fn main() {
    fn process<A>(_value: A) {}
    fn emit<A, B>(__call: A, __zip: B) {}
    emit(process(1), "2024-01-15T12:00:00");
}
