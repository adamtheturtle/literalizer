use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        HashMap::from([("item", "existing")]),
        // This comment describes the next item.
        HashMap::from([("item", "next")]),
    ];
    let _ = &my_data;
    my_data = vec![
        HashMap::from([("item", "existing")]),
        // This comment describes the next item.
        HashMap::from([("item", "next")]),
    ];
    let _ = &mut my_data;
}
