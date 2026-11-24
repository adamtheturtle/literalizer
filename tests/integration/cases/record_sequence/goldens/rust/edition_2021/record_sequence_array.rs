#[derive(Clone)]
pub struct Record0 {
    pub id: i32,
    pub label: &'static str,
    pub tags: [String; 0],
}
fn main() {
    let my_data = [
        Record0 { id: 1, label: "first", tags: [] as [String; 0] },
        Record0 { id: 2, label: "second", tags: [] as [String; 0] },
        Record0 { id: 3, label: "third", tags: [] as [String; 0] },
    ];
    let _ = &my_data;
}
