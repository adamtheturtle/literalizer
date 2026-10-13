use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        HashMap::from([("first", "Alice"), ("last", "Smith")]),
        HashMap::from([("first", "Bob"), ("last", "Jones")]),
    ];
    let _ = &my_data;
}
