use std::collections::HashMap;
#[derive(Clone)]
pub enum Value {
    I32(i32),
    Str(&'static str),
}
#[derive(Clone)]
pub struct Record0 {
    pub input: HashMap<&'static str, Value>,
}
fn main() {
    let my_data = [
        Record0 { input: HashMap::from([("a", Value::I32(1))]) },
        Record0 { input: HashMap::from([("b", Value::Str("two"))]) },
    ];
    let _ = &my_data;
}
