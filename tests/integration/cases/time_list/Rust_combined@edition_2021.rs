use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("times", vec!["09:30:00", "17:45:00", "23:59:59"]),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("times", vec!["09:30:00", "17:45:00", "23:59:59"]),
    ]);
    let _ = &mut my_data;
}
