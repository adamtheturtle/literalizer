use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        HashMap::from([("first", "Alice"), ("last", "Smith")]),
        HashMap::from([("first", "Bob"), ("middle", "Quincy")]),
    ];
    let _ = &my_data;
    my_data = vec![
        HashMap::from([("first", "Alice"), ("last", "Smith")]),
        HashMap::from([("first", "Bob"), ("middle", "Quincy")]),
    ];
    let _ = &mut my_data;
}
