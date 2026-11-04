#[derive(Clone)]
pub struct Record0 {
    pub x: i32,
}
fn main() {
    let my_data = (
        ((1,), Record0 { x: 1 }),
        (Record0 { x: 1 }, Record0 { x: 2 }),
        ((), (Record0 { x: 1 },)),
        ((), ()),
    );
    let _ = &my_data;
}
