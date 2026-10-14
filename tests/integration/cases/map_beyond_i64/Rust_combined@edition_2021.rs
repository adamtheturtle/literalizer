use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("a", 9223372036854775807i128),
        ("b", 9223372036854775808i128),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("a", 9223372036854775807i128),
        ("b", 9223372036854775808i128),
    ]);
    let _ = &mut my_data;
}
