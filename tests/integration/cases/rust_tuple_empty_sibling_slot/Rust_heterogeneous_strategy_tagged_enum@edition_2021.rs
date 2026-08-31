enum Value {
    I32(i32),
    List(Vec<Value>),
}
fn main() {
    let my_data = vec![
        vec![Value::I32(1), Value::List(vec![])],
        vec![Value::I32(2), Value::List(vec![Value::I32(3)])],
    ];
    let _ = my_data;
}
