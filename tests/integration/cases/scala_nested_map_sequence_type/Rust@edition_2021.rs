use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", HashMap::from([("b", vec![1, 2, 3])])),
    ]);
    let _ = my_data;
}
