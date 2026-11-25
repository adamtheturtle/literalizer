use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", 9_223_372_036_854_775_807i128),
        ("b", 9_223_372_036_854_775_808i128),
    ]);
    let _ = &my_data;
}
