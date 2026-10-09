enum Value {
    Str(&'static str),
    I32(i32),
    Bool(bool),
}
fn main() {
    fn process<A>(_value: A) {}
    process(vec![Value::Str("hello"), Value::I32(42), Value::Bool(true)]);
}
