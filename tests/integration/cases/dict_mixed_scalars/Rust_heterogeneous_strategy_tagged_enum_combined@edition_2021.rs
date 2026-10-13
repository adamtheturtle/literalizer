use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
enum Value {
    I32(i32),
    Str(&'static str),
}
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("a", Value::I32(1)),
        ("b", Value::Str("x")),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("a", Value::I32(1)),
        ("b", Value::Str("x")),
    ]);
    let _ = &mut my_data;
}
