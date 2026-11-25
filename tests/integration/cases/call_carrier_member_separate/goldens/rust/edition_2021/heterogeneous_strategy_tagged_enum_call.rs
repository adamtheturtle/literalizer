#[derive(Clone)]
pub enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    struct AppType;
    impl AppType { fn go<A, B>(&self, _first_value: A, _second_value: B) {} }
    let app = AppType;
    app.go(vec![Value::I32(1)], vec![Value::Str("text")]);
}
