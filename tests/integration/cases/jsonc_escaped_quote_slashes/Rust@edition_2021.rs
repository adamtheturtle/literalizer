use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("text", "a\"//b"),
    ]);
    let _ = my_data;
}
