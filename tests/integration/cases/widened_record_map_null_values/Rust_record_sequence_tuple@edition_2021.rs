use std::collections::HashMap;
#[derive(Clone)]
pub enum Value {
    Null,
}
#[derive(Clone)]
pub struct Record0 {
    pub input: HashMap<&'static str, Value>,
}
fn main() {
    let my_data = (
        Record0 { input: HashMap::from([("a", Value::Null)]) },
        Record0 { input: HashMap::from([("b", Value::Null)]) },
    );
    let _ = &my_data;
}
