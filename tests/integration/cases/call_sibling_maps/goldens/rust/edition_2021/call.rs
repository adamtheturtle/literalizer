use std::collections::HashMap;
fn main() {
    fn process<A>(_value: A) {}
    process(HashMap::from([("value", 1)]));
    process(HashMap::from([("value", "hello")]));
}
