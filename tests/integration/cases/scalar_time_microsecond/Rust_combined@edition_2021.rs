use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("exact_millisecond", "09:30:15.123000"),
        ("sub_millisecond", "09:30:15.123456"),
    ]);
    my_data = HashMap::from([
        ("exact_millisecond", "09:30:15.123000"),
        ("sub_millisecond", "09:30:15.123456"),
    ]);
    let _ = my_data;
}
