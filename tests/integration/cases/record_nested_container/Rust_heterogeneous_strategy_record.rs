use std::collections::HashMap;
struct Record0 {
    title: &'static str,
    tags: Vec<&'static str>,
    priority: i32,
}
fn main() {
    let my_data = Record0 {
        title: "report",
        tags: vec![
            "draft",
            "urgent",
            "review",
        ],
        priority: 2,
    };
    let _ = my_data;
}
