use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let userObj = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = userObj;
    let _ = &my_data;
}
