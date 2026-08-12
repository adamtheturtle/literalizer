use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("value", HashMap::from([("$ref", "foo")])),
    ]);
    let _ = my_data;
}
