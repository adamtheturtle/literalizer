use std::collections::HashMap;
fn main() {
    let value = "12:30:15+02:00";
    let my_data = HashMap::from([
        ("x", value),
    ]);
    let _ = &my_data;
}
