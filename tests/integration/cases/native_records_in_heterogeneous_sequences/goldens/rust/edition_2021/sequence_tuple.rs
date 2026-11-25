use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("h", (1, "a", (2, "b"), HashMap::from([("k", (true,))]))),
    ]);
    let _ = &my_data;
}
