use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        HashMap::from([("m", HashMap::<String, String>::from([]))]),
        HashMap::from([("m", HashMap::<String, String>::from([]))]),
    ];
    let _ = &my_data;
}
