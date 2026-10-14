use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("morning", "09:30:00"),
        ("afternoon", "14:15:00"),
        ("evening", "23:59:59"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("morning", "09:30:00"),
        ("afternoon", "14:15:00"),
        ("evening", "23:59:59"),
    ]);
    let _ = &mut my_data;
}
