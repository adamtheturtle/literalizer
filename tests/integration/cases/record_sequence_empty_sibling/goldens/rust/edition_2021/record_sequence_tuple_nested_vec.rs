#[derive(Clone)]
pub struct Record0 {
    pub x: i32,
}
fn main() {
    let my_data = vec![
        vec![],
        vec![Record0 { x: 1 }],
    ];
    let _ = &my_data;
}
