use std::collections::HashMap;
struct Record0 {
    call: &'static str,
    args: (i32, &'static str, &'static str, i32),
}
fn main() {
    let my_data = vec![
        Record0 { call: "send", args: (1, "email", "a@gmail.com", 100) },
        Record0 { call: "recv", args: (2, "sms", "b@example.com", 200) },
    ];
    let _ = my_data;
}
