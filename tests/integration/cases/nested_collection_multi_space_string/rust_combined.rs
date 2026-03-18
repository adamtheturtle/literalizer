use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    {
        let my_data = vec![
            HashMap::from([("key", "hello   world"), ("value", 1)]),
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        HashMap::from([("key", "hello   world"), ("value", 1)]),
    ];
    let _ = my_data;
}
