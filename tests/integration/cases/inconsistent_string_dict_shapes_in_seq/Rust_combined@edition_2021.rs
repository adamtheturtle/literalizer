use std::collections::HashMap;
fn main() {
    let mut my_data = vec![
        HashMap::from([("first", "Alice"), ("last", "Smith")]),
        HashMap::from([("first", "Bob"), ("middle", "Quincy")]),
    ];
    my_data = vec![
        HashMap::from([("first", "Alice"), ("last", "Smith")]),
        HashMap::from([("first", "Bob"), ("middle", "Quincy")]),
    ];
    let _ = my_data;
}
