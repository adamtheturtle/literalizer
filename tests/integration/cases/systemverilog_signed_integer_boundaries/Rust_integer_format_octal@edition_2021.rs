use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("i32_below", -0o20000000001i64),
        ("i32_minimum", -0o20000000000),
        ("i32_above", -0o17777777777),
        ("i32_maximum", 0o17777777777),
        ("i32_over", 0o20000000000i64),
        ("i64_minimum", -0o1000000000000000000000i64),
        ("i64_maximum", 0o777777777777777777777i64),
    ]);
    let _ = my_data;
}
