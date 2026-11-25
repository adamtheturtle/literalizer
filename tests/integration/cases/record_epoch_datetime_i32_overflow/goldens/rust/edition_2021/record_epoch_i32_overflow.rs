#[derive(Clone)]
pub struct Record0 {
    pub within_i32: i64,
    pub beyond_i32: i64,
}
fn main() {
    let my_data = Record0 {
        within_i32: 1705320000,
        beyond_i32: 4085195400i64,
    };
    let _ = &my_data;
}
