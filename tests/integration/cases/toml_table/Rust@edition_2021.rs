use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("section", HashMap::from([("value", 1)])),
    ]);
    let _ = &my_data;
}
