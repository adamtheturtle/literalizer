use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("my-key", "value1"),
        ("another-key", "value2"),
        ("normal_key", "value3"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("my-key", "value1"),
        ("another-key", "value2"),
        ("normal_key", "value3"),
    ]);
    let _ = &mut my_data;
}
