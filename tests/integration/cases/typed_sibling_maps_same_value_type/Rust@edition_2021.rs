use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        HashMap::from([("s", 1)]),
        HashMap::from([("t", 3)]),
    ];
    let _ = &my_data;
}
