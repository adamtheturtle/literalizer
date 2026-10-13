use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("0a", "first"),
        ("1b", "second"),
    ]);
    let _ = &my_data;
}
