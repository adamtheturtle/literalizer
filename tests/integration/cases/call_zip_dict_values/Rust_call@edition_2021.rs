use std::collections::HashMap;
fn main() {
    fn process<A>(_value: A) {}
    fn emit<A, B>(__call: A, __zip: B) {}
    emit(process("hello"), HashMap::from([("a", 1), ("b", 2)]));
    emit(process(42), HashMap::from([("c", 3), ("d", 4)]));
}
