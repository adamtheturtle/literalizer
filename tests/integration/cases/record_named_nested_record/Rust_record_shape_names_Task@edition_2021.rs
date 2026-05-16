use std::collections::HashMap;
struct Task {
    id: i32,
    description: &'static str,
    is_done: bool,
    blocks: Vec<i32>,
}
struct Record0 {
    project: &'static str,
    lead_task: Task,
}
fn main() {
    let my_data = Record0 {
        project: "alpha",
        lead_task: Task {
            id: 100,
            description: "first task",
            is_done: false,
            blocks: vec![
                102,
                103,
            ],
        },
    };
    let _ = my_data;
}
