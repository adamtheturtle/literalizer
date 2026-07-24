use std::collections::HashMap;
struct NamedType {
    id: i32,
    label: &'static str,
    enabled: bool,
    related_ids: Vec<i32>,
}
struct Record0 {
    project: &'static str,
    lead_item: NamedType,
}
fn main() {
    let my_data = Record0 {
        project: "alpha",
        lead_item: NamedType {
            id: 100,
            label: "first item",
            enabled: false,
            related_ids: vec![
                102,
                103,
            ],
        },
    };
    let _ = my_data;
}
