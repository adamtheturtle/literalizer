#[derive(Clone)]
pub struct Record0 {
    pub name: &'static str,
    pub age: i32,
    pub active: bool,
    pub score: f64,
}
fn main() {
    let my_data = Record0 {
        name: "Alice",
        age: 30,
        active: true,
        score: 4.5,
    };
    let _ = &my_data;
}
