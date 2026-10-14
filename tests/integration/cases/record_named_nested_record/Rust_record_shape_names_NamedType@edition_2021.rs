#[derive(Clone)]
pub struct NamedType {
    pub id: i32,
    pub label: &'static str,
    pub enabled: bool,
    pub related_ids: Vec<i32>,
}
#[derive(Clone)]
pub struct Record0 {
    pub collection: &'static str,
    pub featured_entry: NamedType,
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
    let _ = &my_data;
}
