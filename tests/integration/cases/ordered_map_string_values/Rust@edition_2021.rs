use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("first", "one"),
        ("second", "two"),
        ("third", "three"),
    ]);
    let _ = &my_data;
}
