#[derive(Clone)]
pub struct Record0 {
    pub field: i32,
}
fn main() {
    let value = Record0 {
        field: 2,
    };
    let my_data = (
        Record0 { field: 1 },
        value,
    );
    let _ = &my_data;
}
