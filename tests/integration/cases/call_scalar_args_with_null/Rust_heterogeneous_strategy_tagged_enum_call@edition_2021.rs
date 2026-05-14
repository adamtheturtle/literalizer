enum Value {
    Null,
    Str(&'static str),
}
fn main() {
    fn process<A>(_value: A) {}
    process(None::<()>);
    process("hello");
}
