#[derive(Clone)]
pub enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    let my_data = vec![
        vec![Value::I32(1), Value::Str("value")],
        Vec::new(),
    ];
    let _ = &my_data;
}
