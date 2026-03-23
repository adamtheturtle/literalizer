use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("users", vec![HashMap::from([("name", "Bob"), ("tags", "[\"admin\", \"user\"]")]), HashMap::from([("name", "Carol"), ("tags", "[\"guest\"]")])]),
    ]);
    let _ = my_data;
}
