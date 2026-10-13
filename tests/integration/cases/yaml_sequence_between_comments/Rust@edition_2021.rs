use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        HashMap::from([("item", "existing")]),
        // This comment describes the next item.
        HashMap::from([("item", "next")]),
    ];
    let _ = &my_data;
}
