use std::collections::HashMap;
fn main() {
    let mut my_data = vec![
        HashMap::from([("first", "Alice"), ("last", "Smith"), ("middle", "Jane")]),
        HashMap::from([("first", "Bob"), ("last", "Jones"), ("middle", "None")]),
    ];
    my_data = vec![
        HashMap::from([("first", "Alice"), ("last", "Smith"), ("middle", "Jane")]),
        HashMap::from([("first", "Bob"), ("last", "Jones"), ("middle", "None")]),
    ];
    let _ = my_data;
}
