enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = vec![
        Value::I32(1),
        Value::Str("email"),
        Value::Str("a@gmail.com"),
        Value::I32(100),
    ];
    let _ = my_data;
}
