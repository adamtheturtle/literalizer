use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("a", 1)]),
        <HashMap<&str, i32>>::from([]),
    ];
    let _ = my_data;
}
