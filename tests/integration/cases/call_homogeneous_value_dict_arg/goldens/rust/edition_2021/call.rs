use std::collections::HashMap;
fn main() {
    fn process<A>(_value: A) {}
    process(HashMap::from([("a", 1), ("b", 2)]));
}
