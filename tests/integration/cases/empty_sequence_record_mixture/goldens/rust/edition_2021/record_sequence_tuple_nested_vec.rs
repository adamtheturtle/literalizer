#[derive(Clone)]
pub struct Record0 {
    pub x: i32,
}
fn main() {
    let my_data = (
        Vec::<String>::new(),
        Record0 {
            x: 1,
        },
    );
    let _ = &my_data;
}
