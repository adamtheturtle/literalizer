use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let shared = [
        HashMap::from([("value", 1)]),
    ];
    let my_data = [
        shared.clone(),
        shared.clone(),
    ];
    let _ = &my_data;
}
