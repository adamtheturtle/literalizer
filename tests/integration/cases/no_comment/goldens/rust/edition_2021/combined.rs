use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("message", "no comment here"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("message", "no comment here"),
    ]);
    let _ = &mut my_data;
}
