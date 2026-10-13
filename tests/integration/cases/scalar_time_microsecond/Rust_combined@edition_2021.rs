use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("exact_millisecond", "09:30:15.123000"),
        ("sub_millisecond", "09:30:15.123456"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("exact_millisecond", "09:30:15.123000"),
        ("sub_millisecond", "09:30:15.123456"),
    ]);
    let _ = &mut my_data;
}
