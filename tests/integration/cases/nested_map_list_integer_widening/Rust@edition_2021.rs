use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("a", vec![1]),
        ("b", vec![1099511627776i64]),
    ]);
    let _ = &my_data;
}
