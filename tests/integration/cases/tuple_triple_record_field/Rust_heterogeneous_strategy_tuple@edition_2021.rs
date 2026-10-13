#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    call: &'static str,
    args: (i32, &'static str, bool),
}
#[allow(non_snake_case)]
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
