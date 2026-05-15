use std::collections::HashMap;
struct Record1 {
    id: i32,
    count: Option<i32>,
}
struct Record0 {
    items: Vec<Record1>,
}
fn main() {
    let my_data = Record0 {
        items: vec![
            Record1 {
                id: 1,
                count: None,
            },
            Record1 {
                id: 2,
                count: Some(10),
            },
            Record1 {
                id: 3,
                count: Some(20),
            },
        ],
    };
    let _ = my_data;
}
