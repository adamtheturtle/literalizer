use std::collections::HashMap;
fn main() {
    {
        let mut my_data = vec![
            HashMap::from([("x", "1"), ("y", "2.5")]),
            HashMap::from([("x", "3"), ("y", "4.0")]),
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        HashMap::from([("x", "1"), ("y", "2.5")]),
        HashMap::from([("x", "3"), ("y", "4.0")]),
    ];
    let _ = my_data;
}
