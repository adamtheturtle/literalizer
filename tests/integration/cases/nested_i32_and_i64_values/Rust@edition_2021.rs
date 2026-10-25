use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("values", vec![1, 2147483648i64]),
    ]);
    let _ = &my_data;
}
