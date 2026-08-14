use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("explicit_string", "5"),
        ("six", "explicitly tagged key"),
    ]);
    let _ = my_data;
}
