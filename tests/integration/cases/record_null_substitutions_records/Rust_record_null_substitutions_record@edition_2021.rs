use std::collections::HashMap;
struct Record0 {
    due_date: i32,
    parent_id: i32,
    assignee: &'static str,
}
fn main() {
    let my_data = vec![
        Record0 { due_date: -1, parent_id: -1, assignee: "" },
        Record0 { due_date: 10, parent_id: 20, assignee: "alice" },
    ];
    let _ = my_data;
}
