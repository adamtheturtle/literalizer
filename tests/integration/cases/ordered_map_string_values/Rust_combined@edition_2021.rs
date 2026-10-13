use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("first", "one"),
        ("second", "two"),
        ("third", "three"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("first", "one"),
        ("second", "two"),
        ("third", "three"),
    ]);
    let _ = &mut my_data;
}
