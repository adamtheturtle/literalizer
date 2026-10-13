use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("exact_millisecond", "09:30:15.123000"),
        ("sub_millisecond", "09:30:15.123456"),
    ]);
    let _ = &my_data;
}
