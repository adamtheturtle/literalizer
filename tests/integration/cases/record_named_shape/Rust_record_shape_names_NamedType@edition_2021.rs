use std::collections::HashMap;
struct NamedType {
    id: i32,
    description: &'static str,
    is_done: bool,
    blocks: Vec<i32>,
}
fn main() {
    let my_data = vec![
        NamedType { id: 100, description: "first task", is_done: false, blocks: vec![102, 103] },
        NamedType { id: 101, description: "second task", is_done: true, blocks: vec![100] },
    ];
    let _ = my_data;
}
