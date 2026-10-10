use std::collections::HashMap;
fn main() {
    let shared = vec![
        1,
        2,
    ];
    let my_data = vec![
        HashMap::from([("left", shared.clone()), ("right", shared.clone())]),
    ];
    let _ = my_data;
}
