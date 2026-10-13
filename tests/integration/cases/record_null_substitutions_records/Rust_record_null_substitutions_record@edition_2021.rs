#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    due_date: i32,
    parent_id: i32,
    assignee: &'static str,
}
#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        Record0 { due_date: -1, parent_id: -1, assignee: "" },
        Record0 { due_date: 10, parent_id: 20, assignee: "alice" },
    ];
    let _ = &my_data;
}
