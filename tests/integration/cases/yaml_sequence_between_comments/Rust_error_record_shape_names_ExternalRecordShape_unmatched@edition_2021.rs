use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("item", "existing")]),
        // This comment describes the next item.
        HashMap::from([("item", "next")]),
    ];
    let _ = my_data;
}
