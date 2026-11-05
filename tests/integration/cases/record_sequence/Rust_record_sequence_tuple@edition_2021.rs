#[derive(Clone)]
pub struct Record0 {
    pub id: i32,
    pub label: &'static str,
    pub tags: (),
}
fn main() {
    let my_data = (
        Record0 { id: 1, label: "first", tags: () },
        Record0 { id: 2, label: "second", tags: () },
        Record0 { id: 3, label: "third", tags: () },
    );
    let _ = &my_data;
}
