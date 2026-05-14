enum Value {
    Str(&'static str),
    I32(i32),
    Bool(bool),
}
fn main() {
    fn process<A, B>(_value: A, _label: B) {}
    process("hello", "a");
    process(42, "b");
    process(true, "c");
}
