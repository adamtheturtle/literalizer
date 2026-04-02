use std::collections::HashMap;
fn main() {
    {
        let mut my_data = vec![
            HashMap::from([("key", "hello   world"), ("value", "1")]),
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        HashMap::from([("key", "hello   world"), ("value", "1")]),
    ];
    let _ = my_data;
}
