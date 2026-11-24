use std::collections::HashMap;
fn main() {
    let my_data = vec![
        vec![HashMap::from([("a", 1)])],
        vec![HashMap::from([("a", 2)])],
    ];
    let _ = &my_data;
}
