use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let item_var = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = HashMap::from([
        ("items", vec![item_var, HashMap::from([("fallback", "value")])]),
    ]);
    let _ = &my_data;
}
