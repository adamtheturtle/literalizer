use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("i32_below", -2_147_483_649i64),
        ("i32_minimum", -2_147_483_648),
        ("i32_above", -2_147_483_647),
        ("i32_maximum", 2_147_483_647),
        ("i32_over", 2_147_483_648i64),
        ("i64_minimum", -9_223_372_036_854_775_808i64),
        ("i64_maximum", 9_223_372_036_854_775_807i64),
    ]);
    let _ = &my_data;
}
