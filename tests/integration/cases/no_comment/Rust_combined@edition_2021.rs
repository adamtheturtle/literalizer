use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("message", "no comment here"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("message", "no comment here"),
    ]);
    let _ = &mut my_data;
}
