use std::collections::HashMap;
struct Record1 {
    id: i32,
    name: &'static str,
}
struct Record2 {
    title: &'static str,
    tags: Vec<&'static str>,
}
struct Record0 {
    user: Record1,
    project: Record2,
}
fn main() {
    let my_data = Record0 {
        user: Record1 {
            id: 1,
            name: "Alice",
        },
        project: Record2 {
            title: "report",
            tags: vec![
                "draft",
                "urgent",
            ],
        },
    };
    let _ = my_data;
}
