enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = vec![
        vec![Value::I32(1), Value::I32(2)],
        vec![Value::Str("a"), Value::Str("b")],
    ];
    let _ = my_data;
}
