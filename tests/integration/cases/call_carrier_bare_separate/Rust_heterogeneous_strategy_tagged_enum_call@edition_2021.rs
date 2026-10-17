#[derive(Clone)]
pub enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    fn make_widget<A, B>(_first_value: A, _second_value: B) {}
    make_widget(vec![Value::I32(1)], vec![Value::Str("text")]);
}
