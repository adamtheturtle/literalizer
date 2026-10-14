use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("a", 1),
        ("b", 1099511627776i64),
    ]);
    let _ = &mut my_data;
}
