use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("times", vec!["09:30:00", "17:45:00", "23:59:59"]),
    ]);
    my_data = HashMap::from([
        ("times", vec!["09:30:00", "17:45:00", "23:59:59"]),
    ]);
    let _ = my_data;
}
