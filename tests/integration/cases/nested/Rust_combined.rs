use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("users", vec![HashMap::from([("name", "Bob"), ("tags", "[\"admin\", \"user\"]")]), HashMap::from([("name", "Carol"), ("tags", "[\"guest\"]")])]),
    ]);
    my_data = HashMap::from([
        ("users", vec![HashMap::from([("name", "Bob"), ("tags", "[\"admin\", \"user\"]")]), HashMap::from([("name", "Carol"), ("tags", "[\"guest\"]")])]),
    ]);
    let _ = my_data;
}
