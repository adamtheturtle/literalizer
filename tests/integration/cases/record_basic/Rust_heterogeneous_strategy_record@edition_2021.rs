#[derive(Clone)]
pub struct Record0 {
    pub id: i32,
    pub label: &'static str,
    pub enabled: bool,
    pub related_ids: Vec<i32>,
}
fn main() {
    let my_data = Record0 {
        id: 1,
        label: "She said \"hello\", then waved",
        enabled: false,
        related_ids: vec![
            1,
            2,
            3,
        ],
    };
    let _ = &my_data;
}
