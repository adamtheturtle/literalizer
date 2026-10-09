use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("i32_below", -0x80000001i64),
        ("i32_minimum", -0x80000000),
        ("i32_above", -0x7fffffff),
        ("i32_maximum", 0x7fffffff),
        ("i32_over", 0x80000000i64),
        ("i64_minimum", -0x8000000000000000i64),
        ("i64_maximum", 0x7fffffffffffffffi64),
    ]);
    let _ = my_data;
}
