use std::collections::HashMap;
fn main() {
    fn consume<A>(_value: A) {}
    let item = 42;
    consume(HashMap::from([("field", item)]));
}
