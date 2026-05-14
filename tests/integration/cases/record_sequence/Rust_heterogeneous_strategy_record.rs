use std::collections::HashMap;
struct Record0 {
    id: i32,
    label: &'static str,
}
fn main() {
    let my_data = vec![
        Record0 { id: 1, label: "first" },
        Record0 { id: 2, label: "second" },
        Record0 { id: 3, label: "third" },
    ];
    let _ = my_data;
}
