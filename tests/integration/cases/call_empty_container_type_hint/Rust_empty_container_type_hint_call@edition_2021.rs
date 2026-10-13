use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
enum Value {
    I32(i32),
    Map(HashMap<String, String>),
}
#[allow(non_snake_case)]
fn main() {
    fn process<A, B>(_values: A, _count: B) {}
    process(vec![Value::I32(1), Value::Map(HashMap::new())], 42);
}
