use std::collections::HashMap;
#[allow(non_snake_case)]
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
