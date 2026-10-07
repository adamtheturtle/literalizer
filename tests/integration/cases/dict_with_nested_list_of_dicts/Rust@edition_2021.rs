use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", vec![vec![HashMap::from([("b", 1)])]]),
    ]);
    let _ = my_data;
}
