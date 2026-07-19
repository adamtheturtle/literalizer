enum Value {
    I32(i32),
    List(Vec<Value>),
}
fn main() {
    let my_data = vec![
        Value::I32(1),
        Value::List(vec![]),
    ];
    let _ = my_data;
}
