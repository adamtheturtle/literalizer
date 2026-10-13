use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        HashMap::from([("m", HashMap::from([("x", 1)]))]),
        HashMap::from([("m", <HashMap<&str, i32>>::from([]))]),
    ];
    let _ = &my_data;
}
