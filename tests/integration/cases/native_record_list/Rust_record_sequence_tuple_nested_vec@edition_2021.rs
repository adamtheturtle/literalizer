#[derive(Clone)]
pub struct Record1 {
    pub age: i32,
}
#[derive(Clone)]
pub struct Record0 {
    pub name: &'static str,
    pub active: bool,
    pub count: i32,
    pub score: f64,
    pub missing: Option<()>,
    pub scores: Vec<i32>,
    pub child: Record1,
}
fn main() {
    let my_data = vec![
        Record0 { name: "Ada", active: true, count: 1, score: 1.5, missing: None::<()>, scores: vec![1, 2], child: Record1 { age: 3 } },
        Record0 { name: "Bob", active: false, count: 2, score: 2.5, missing: None::<()>, scores: vec![4], child: Record1 { age: 5 } },
    ];
    let _ = &my_data;
}
