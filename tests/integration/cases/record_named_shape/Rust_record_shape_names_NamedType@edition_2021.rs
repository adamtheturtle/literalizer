#[derive(Clone)]
pub struct NamedType {
    pub id: i32,
    pub label: &'static str,
    pub enabled: bool,
    pub related_ids: Vec<i32>,
}
fn main() {
    let my_data = vec![
        NamedType { id: 100, label: "first entry", enabled: false, related_ids: vec![102, 103] },
        NamedType { id: 101, label: "second entry", enabled: true, related_ids: vec![100] },
    ];
    let _ = &my_data;
}
