use std::collections::HashMap;
fn main() {
    let shared = [
        HashMap::from([("value", 1)]),
    ];
    let my_data = [
        shared.clone(),
        shared.clone(),
    ];
    let _ = my_data;
}
