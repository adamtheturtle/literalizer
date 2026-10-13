use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let shared = vec![
        1,
        2,
    ];
    let my_data = vec![
        HashMap::from([("left", shared.clone()), ("right", shared.clone())]),
    ];
    let _ = &my_data;
}
