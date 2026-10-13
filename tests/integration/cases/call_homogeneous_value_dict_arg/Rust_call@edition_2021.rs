use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    fn process<A>(_value: A) {}
    process(HashMap::from([("a", 1), ("b", 2)]));
}
