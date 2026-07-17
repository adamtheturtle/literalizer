use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", 9223372036854775807i128),
        ("b", 9223372036854775808i128),
    ]);
    let _ = my_data;
}
