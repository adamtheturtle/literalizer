use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("value", HashMap::from([("$ref", "foo")])),
    ]);
    my_data = HashMap::from([
        ("value", HashMap::from([("$ref", "foo")])),
    ]);
    let _ = my_data;
}
