#[derive(Clone)]
pub struct Record0 {
    pub call: &'static str,
    pub args: (i32, &'static str, &'static str, i32),
}
fn main() {
    let mut my_data = Record0 {
        call: "send",
        args: (
            1,
            "email",
            "a@gmail.com",
            100,
        ),
    };
    let _ = &my_data;
    my_data = Record0 {
        call: "send",
        args: (
            1,
            "email",
            "a@gmail.com",
            100,
        ),
    };
    let _ = &mut my_data;
}
