use std::collections::HashMap;
struct Record0 {
    call: &'static str,
    args: (i32, &'static str, bool),
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
    let _ = my_data;
}
