#[derive(Clone)]
pub enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    fn f<A>(_a: A) {}
    f(vec![Value::I32(1), Value::Str("x")]);
}
