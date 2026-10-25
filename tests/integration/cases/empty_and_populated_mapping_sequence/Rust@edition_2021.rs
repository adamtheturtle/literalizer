use std::collections::HashMap;
fn main() {
    let my_data = vec![
        <HashMap<&str, i32>>::from([]),
        HashMap::from([("value", 1)]),
    ];
    let _ = &my_data;
}
