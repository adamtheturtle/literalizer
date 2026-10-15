use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("positive", [HashMap::from([("item", [2147483648i64])])]),
        ("negative", [HashMap::from([("item", [-2147483649i64])])]),
        ("mixed", [HashMap::from([("item", [0, 2147483648i64])])]),
    ]);
    let _ = &my_data;
}
