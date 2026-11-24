#[derive(Clone)]
pub enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    fn make_widget<A, B, C>(_before: A, _populated: B, _after: C) {}
    make_widget(Vec::<String>::new(), vec![Value::I32(1)], Vec::<String>::new());
    make_widget(vec![Value::Str("text")], vec![Value::I32(2)], Vec::<String>::new());
    make_widget(Vec::<String>::new(), vec![Value::Str("text")], Vec::<String>::new());
    make_widget(vec![Value::Str("text")], vec![Value::I32(2)], vec![Value::I32(3)]);
}
