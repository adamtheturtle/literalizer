#[derive(Clone)]
pub enum Value {
    I32(i32),
    Str(&'static str),
}
fn main() {
    struct ThingType;
    impl ThingType { fn go<A, B, C>(&self, _before: A, _populated: B, _after: C) {} }
    let thing = ThingType;
    thing.go(Vec::<String>::new(), vec![Value::I32(1)], Vec::<String>::new());
    thing.go(vec![Value::Str("text")], vec![Value::I32(2)], Vec::<String>::new());
    thing.go(Vec::<String>::new(), vec![Value::Str("text")], Vec::<String>::new());
    thing.go(vec![Value::Str("text")], vec![Value::I32(2)], vec![Value::I32(3)]);
}
