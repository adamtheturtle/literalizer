#[derive(Clone)]
pub struct Record0 {
    pub scores: (i32, i32, i32),
    pub args: (i32, &'static str, &'static str, i32),
}
fn main() {
    let my_data = Record0 {
        scores: (
            10,
            20,
            30,
        ),
        args: (
            1,
            "email",
            "a@gmail.com",
            100,
        ),
    };
    let _ = &my_data;
}
