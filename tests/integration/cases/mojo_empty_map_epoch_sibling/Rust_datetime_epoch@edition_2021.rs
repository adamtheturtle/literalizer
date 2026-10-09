use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("timestamp", 1577836800)]),
        <HashMap<&str, i64>>::from([]),
    ];
    let _ = my_data;
}
