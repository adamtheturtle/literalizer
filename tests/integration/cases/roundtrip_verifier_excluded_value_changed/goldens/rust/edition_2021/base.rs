use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("keep", true),
        ("skip", false),
    ]);
    let _ = &my_data;
}
