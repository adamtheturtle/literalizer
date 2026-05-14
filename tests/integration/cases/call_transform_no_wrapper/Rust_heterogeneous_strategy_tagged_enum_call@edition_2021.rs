enum Value {
    Str(&'static str),
    I32(i32),
    Bool(bool),
}
fn main() {
    fn process<A>(_value: A) {}
    process("hello");
    process(42);
    process(true);
}
