use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", 0o777777777777777777777i128),
        ("b", 0o1000000000000000000000i128),
    ]);
    let _ = &my_data;
}
