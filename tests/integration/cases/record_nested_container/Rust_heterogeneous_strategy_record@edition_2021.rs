#[derive(Clone)]
pub struct Record0 {
    pub title: &'static str,
    pub tags: Vec<&'static str>,
    pub priority: i32,
}
fn main() {
    let my_data = Record0 {
        title: "report",
        tags: vec![
            "draft",
            "urgent",
            "review",
        ],
        priority: 2,
    };
    let _ = &my_data;
}
