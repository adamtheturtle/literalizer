use std::collections::HashMap;
#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    input: HashMap<&'static str, i32>,
}
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        Record0 {
            input: HashMap::from([
                ("a", 1),
            ]),
        },
        Record0 {
            input: HashMap::from([
                ("b", 2),
            ]),
        },
    ];
    let _ = &my_data;
}
