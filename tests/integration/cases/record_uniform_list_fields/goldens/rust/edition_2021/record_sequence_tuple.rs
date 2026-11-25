#[derive(Clone)]
pub struct Record0 {
    pub scores: (i32, i32),
}
fn main() {
    let my_data = (
        Record0 { scores: (1, 2) },
        Record0 { scores: (3, 4) },
    );
    let _ = &my_data;
}
