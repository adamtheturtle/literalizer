#[derive(Clone)]
pub struct Record0 {
    pub id: i32,
    pub label: &'static str,
    pub tags: Vec<String>,
}
fn main() {
    let my_data = vec![
        Record0 { id: 1, label: "first", tags: Vec::<String>::new() },
        Record0 { id: 2, label: "second", tags: Vec::<String>::new() },
        Record0 { id: 3, label: "third", tags: Vec::<String>::new() },
    ];
    let _ = &my_data;
}
