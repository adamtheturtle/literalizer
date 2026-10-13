use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("message", "no comment here"),
    ]);
    let _ = &my_data;
}
