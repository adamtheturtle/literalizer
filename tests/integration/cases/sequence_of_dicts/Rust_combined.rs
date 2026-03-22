use std::collections::{HashMap};
fn main() {
    {
        let my_data = vec![
            HashMap::from([("name", "Alice"), ("age", "30")]),
            HashMap::from([("name", "Bob"), ("age", "25")]),
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        HashMap::from([("name", "Alice"), ("age", "30")]),
        HashMap::from([("name", "Bob"), ("age", "25")]),
    ];
    let _ = my_data;
}
