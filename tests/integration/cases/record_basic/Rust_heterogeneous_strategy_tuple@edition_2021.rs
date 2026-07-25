use std::collections::HashMap;
struct Record0 {
    id: i32,
    label: &'static str,
    enabled: bool,
    related_ids: Vec<i32>,
}
fn main() {
    let my_data = Record0 {
        id: 1,
        label: "She said \"hello\", then waved",
        enabled: false,
        related_ids: vec![
            1,
            2,
            3,
        ],
    };
    let _ = my_data;
}
