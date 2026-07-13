use std::collections::HashMap;
struct Record0 {
    r#type: &'static str,
    r#match: &'static str,
    id: i32,
}
fn main() {
    let my_data = vec![
        Record0 { r#type: "a", r#match: "b", id: 1 },
    ];
    let _ = my_data;
}
