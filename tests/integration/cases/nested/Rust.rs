use std::collections::HashMap;
fn main() {
    let _ = HashMap::from([
        ("users", vec![HashMap::from([("name", "Bob"), ("tags", "[\"admin\", \"user\"]")]), HashMap::from([("name", "Carol"), ("tags", "[\"guest\"]")])]),
    ]);
}
