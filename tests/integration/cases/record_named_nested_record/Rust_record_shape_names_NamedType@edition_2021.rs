use std::collections::HashMap;
struct NamedType {
    id: i32,
    label: &'static str,
    enabled: bool,
    related_ids: Vec<i32>,
}
struct Record0 {
    collection: &'static str,
    featured_entry: NamedType,
}
fn main() {
    let my_data = Record0 {
        collection: "alpha",
        featured_entry: NamedType {
            id: 100,
            label: "first entry",
            enabled: false,
            related_ids: vec![
                102,
                103,
            ],
        },
    };
    let _ = my_data;
}
