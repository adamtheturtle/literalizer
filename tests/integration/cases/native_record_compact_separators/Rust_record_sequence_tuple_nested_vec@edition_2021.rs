#[derive(Clone)]
pub struct Record0 {
    pub name: &'static str,
    pub active: bool,
}
fn main() {
    let my_data = vec![
        Record0 { name: "Ada", active: true },
    ];
    let _ = &my_data;
}
