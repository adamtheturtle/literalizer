use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    fn process<A>(_value: A) {}
    process(HashMap::from([("value", Value::I32(1))]));
    process(HashMap::from([("value", Value::Str("hello"))]));
}
