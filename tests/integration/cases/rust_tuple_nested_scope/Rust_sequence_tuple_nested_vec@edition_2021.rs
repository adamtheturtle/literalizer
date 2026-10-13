use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("x", (1, (2, vec![3]))),
    ]);
    let _ = &my_data;
}
