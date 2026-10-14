#[derive(Clone)]
pub struct Record0 {
    pub short: (i32,),
    pub long: (i32, i32),
}
fn main() {
    let my_data = Record0 {
        short: (
            1,
        ),
        long: (
            1,
            2,
        ),
    };
    let _ = &my_data;
}
