use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("", "unnamed"),
        ("named", "value"),
    ]);
    let _ = &my_data;
}
