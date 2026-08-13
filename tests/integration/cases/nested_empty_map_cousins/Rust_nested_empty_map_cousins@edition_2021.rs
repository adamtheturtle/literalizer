use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("m", HashMap::from([("x", 1)]))]),
        HashMap::from([("m", <HashMap<&str, i32>>::from([]))]),
    ];
    let _ = my_data;
}
