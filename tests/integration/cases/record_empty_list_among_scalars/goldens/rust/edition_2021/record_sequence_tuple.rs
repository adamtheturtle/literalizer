#[derive(Clone)]
pub struct Record0 {
    pub a: (i32, ()),
}
fn main() {
    let my_data = Record0 {
        a: (
            1,
            (),
        ),
    };
    let _ = &my_data;
}
