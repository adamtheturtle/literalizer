enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = vec![
        vec![Value::I32(1), Value::Str("a")],
        vec![Value::I32(2), Value::Str("b")],
    ];
    let _ = my_data;
}
