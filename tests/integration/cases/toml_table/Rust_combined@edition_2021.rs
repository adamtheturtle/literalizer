use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("section", HashMap::from([("value", 1)])),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("section", HashMap::from([("value", 1)])),
    ]);
    let _ = &mut my_data;
}
