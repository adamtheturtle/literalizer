use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("a", vec![1]),
        ("b", vec![]),
    ]);
    let _ = &my_data;
}
