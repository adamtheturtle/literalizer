#[allow(dead_code)]
#[derive(Clone)]
enum Value {
    I32(i32),
    List(Vec<Value>),
}
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        Value::I32(1),
        Value::List(vec![]),
    ];
    let _ = &my_data;
}
