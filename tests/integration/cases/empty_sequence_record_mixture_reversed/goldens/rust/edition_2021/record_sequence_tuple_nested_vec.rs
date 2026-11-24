#[derive(Clone)]
pub struct Record0 {
    pub x: i32,
}
fn main() {
    let my_data = (
        Record0 {
            x: 1,
        },
        Vec::<String>::new(),
    );
    let _ = &my_data;
}
