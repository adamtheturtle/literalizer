#[derive(Clone)]
pub struct Record0 {
    pub active: bool,
}
fn main() {
    let my_data = [
        Record0 { active: true },
        Record0 { active: false },
    ];
    let _ = &my_data;
}
