use std::collections::HashMap;
enum Value {
    I32(i32),
    Map(HashMap<String, String>),
}
fn main() {
    fn process<A, B>(_values: A, _count: B) {}
    process(vec![Value::I32(1), Value::Map(<HashMap<String, String>>::new())], 42);
}
