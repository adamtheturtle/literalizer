use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("i32_below", -2147483649i64),
        ("i32_minimum", -2147483648),
        ("i32_above", -2147483647),
        ("i32_maximum", 2147483647),
        ("i32_over", 2147483648i64),
        ("i64_minimum", -9223372036854775808i64),
        ("i64_maximum", 9223372036854775807i64),
    ]);
    let _ = my_data;
}
