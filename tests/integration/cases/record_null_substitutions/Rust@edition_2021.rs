use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("rows", vec![HashMap::from([("replacement", -1), ("present", 1)]), HashMap::from([("replacement", 2), ("present", 3)])]),
    ]);
    let _ = my_data;
}
