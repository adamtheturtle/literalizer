use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        vec![HashMap::from([("name", "Alice")]), HashMap::from([("name", "Bob")])],
        vec![HashMap::from([("name", "Charlie")]), HashMap::from([("name", "Dave")])],
    ];
    let _ = &my_data;
    my_data = vec![
        vec![HashMap::from([("name", "Alice")]), HashMap::from([("name", "Bob")])],
        vec![HashMap::from([("name", "Charlie")]), HashMap::from([("name", "Dave")])],
    ];
    let _ = &mut my_data;
}
