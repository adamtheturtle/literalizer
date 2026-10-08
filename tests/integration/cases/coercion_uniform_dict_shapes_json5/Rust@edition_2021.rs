use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("type", "create"), ("name", "a")]),
        HashMap::from([("type", "update"), ("name", "b")]),
    ];
    let _ = my_data;
}
