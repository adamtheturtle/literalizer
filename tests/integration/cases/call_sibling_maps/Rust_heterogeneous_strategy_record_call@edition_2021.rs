use std::collections::HashMap;
struct Record0 {
    value: i32,
}
struct Record1 {
    value: &'static str,
}
fn main() {
    fn process<A>(_value: A) {}
    process(HashMap::from([("value", 1)]));
    process(HashMap::from([("value", "hello")]));
}
