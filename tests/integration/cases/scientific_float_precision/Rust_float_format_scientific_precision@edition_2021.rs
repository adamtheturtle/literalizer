use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("value", 1.2345678901234567),
    ]);
    let _ = &my_data;
}
