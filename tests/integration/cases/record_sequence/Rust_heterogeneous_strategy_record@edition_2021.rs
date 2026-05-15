use std::collections::HashMap;
struct Record0 {
    id: i32,
    label: &'static str,
    tags: Vec<String>,
}
fn main() {
    let my_data = vec![
        Record0 { id: 1, label: "first", tags: Vec::<String>::new() },
        Record0 { id: 2, label: "second", tags: Vec::<String>::new() },
        Record0 { id: 3, label: "third", tags: Vec::<String>::new() },
    ];
    let _ = my_data;
}
