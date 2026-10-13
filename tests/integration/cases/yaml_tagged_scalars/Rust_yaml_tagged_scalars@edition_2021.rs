use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("explicit_string", "5"),
        ("six", "explicitly tagged key"),
    ]);
    let _ = &my_data;
}
