use std::collections::HashMap;
struct Record0 {
    vals: (&'static str, &'static str),
}
fn main() {
    let my_data = Record0 {
        vals: (
            "09:30:00",
            "hello",
        ),
    };
    let _ = my_data;
}
