use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("first", "one"),
        ("second", "two"),
        ("third", "three"),
    ]);
    my_data = HashMap::from([
        ("first", "one"),
        ("second", "two"),
        ("third", "three"),
    ]);
    let _ = my_data;
}
