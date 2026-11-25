#[derive(Clone)]
pub struct Record0 {
    pub active: bool,
}
fn main() {
    let my_data = vec![
        Record0 { active: true },
        Record0 { active: false },
    ];
    let _ = &my_data;
}
