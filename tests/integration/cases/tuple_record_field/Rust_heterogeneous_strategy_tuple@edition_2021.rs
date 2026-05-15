use std::collections::HashMap;
struct Record0 {
    call: &'static str,
    args: (i32, &'static str, &'static str, i32),
}
fn main() {
    let my_data = Record0 {
        call: "send",
        args: (
            1,
            "email",
            "a@gmail.com",
            100,
        ),
    };
    let _ = my_data;
}
