#[derive(Clone)]
pub struct Record0 {
    pub call: &'static str,
    pub args: (i32, &'static str, bool),
}
fn main() {
    let my_data = Record0 {
        call: "send",
        args: (
            1,
            "email",
            true,
        ),
    };
    let _ = &my_data;
}
