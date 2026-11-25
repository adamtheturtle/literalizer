// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
use std::collections::HashMap;
fn main() {
    let userObj = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = userObj;
    let _ = &my_data;
}
