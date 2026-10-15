use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", (HashMap::from([("item", (1,))]),)),
        ("b", (HashMap::from([("item", (2,))]),)),
    ]);
    let _ = &my_data;
}
