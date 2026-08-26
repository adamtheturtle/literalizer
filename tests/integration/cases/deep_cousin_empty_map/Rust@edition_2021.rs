use std::collections::HashMap;
fn main() {
    let my_data = vec![
        HashMap::from([("outer", HashMap::from([("inner", HashMap::from([("x", 1)]))]))]),
        HashMap::from([("outer", HashMap::from([("inner", <HashMap<&str, i32>>::from([]))]))]),
    ];
    let _ = my_data;
}
