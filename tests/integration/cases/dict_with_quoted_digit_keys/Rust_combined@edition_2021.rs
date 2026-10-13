use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("0a", "first"),
        ("1b", "second"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("0a", "first"),
        ("1b", "second"),
    ]);
    let _ = &mut my_data;
}
