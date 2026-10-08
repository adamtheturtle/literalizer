use std::collections::HashMap;
fn main() {
    let sibling_map = HashMap::from([
        ("k", 2),
    ]);
    let my_data = vec![
        HashMap::from([("k", 1)]),
        sibling_map,
    ];
    let _ = my_data;
}
