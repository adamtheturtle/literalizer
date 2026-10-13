#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    within_i32: i64,
    beyond_i32: i64,
}
#[allow(non_snake_case)]
fn main() {
    let my_data = Record0 {
        within_i32: 1705320000,
        beyond_i32: 4085195400i64,
    };
    let _ = &my_data;
}
