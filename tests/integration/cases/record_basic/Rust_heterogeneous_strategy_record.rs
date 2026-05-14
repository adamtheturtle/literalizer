use std::collections::HashMap;
struct Record0 {
    id: i32,
    description: &'static str,
    is_done: bool,
    blocks: Vec<i32>,
}
fn main() {
    let my_data = Record0 {
        id: 1,
        description: "She said \"hello\", then waved",
        is_done: false,
        blocks: vec![
            1,
            2,
            3,
        ],
    };
    let _ = my_data;
}
