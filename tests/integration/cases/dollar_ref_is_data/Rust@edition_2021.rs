use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("value", HashMap::from([("$ref", "foo")])),
    ]);
    let _ = &my_data;
}
