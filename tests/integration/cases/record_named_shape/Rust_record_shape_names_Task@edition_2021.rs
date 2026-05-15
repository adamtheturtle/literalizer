use std::collections::HashMap;
struct Task {
    id: i32,
    description: &'static str,
    is_done: bool,
    blocks: Vec<i32>,
}
fn main() {
    let my_data = vec![
        Task { id: 100, description: "first task", is_done: false, blocks: vec![102, 103] },
        Task { id: 101, description: "second task", is_done: true, blocks: Vec::<String>::new() },
    ];
    let _ = my_data;
}
