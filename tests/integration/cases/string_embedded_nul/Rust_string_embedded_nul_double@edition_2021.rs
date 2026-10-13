use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("x", "\0"),
        ("y", "\01"),
    ]);
    let _ = &my_data;
}
