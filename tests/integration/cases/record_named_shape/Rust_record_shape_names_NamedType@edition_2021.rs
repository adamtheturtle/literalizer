use std::collections::HashMap;
struct NamedType {
    id: i32,
    label: &'static str,
    enabled: bool,
    related_ids: Vec<i32>,
}
fn main() {
    let my_data = vec![
        NamedType { id: 100, label: "first item", enabled: false, related_ids: vec![102, 103] },
        NamedType { id: 101, label: "second item", enabled: true, related_ids: vec![100] },
    ];
    let _ = my_data;
}
