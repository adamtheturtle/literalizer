use std::collections::HashMap;
fn main() {
    fn process<A>(_data: A) {}
    let my_var = 42;
    process(HashMap::from([("key", my_var), ("count", 42)]));
}
