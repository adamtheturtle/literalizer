#[derive(Clone)]
enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let shared = vec![
        Value::I32(1),
        Value::Str("x"),
    ];
    let my_data = vec![
        shared.clone(),
        shared.clone(),
    ];
    let _ = my_data;
}
