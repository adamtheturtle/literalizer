use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("missing", -1), ("present", 1)]),
        HashMap::from([("missing", 2), ("present", 3)]),
    ];
    let _ = my_data;
}
