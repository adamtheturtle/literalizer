use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("starts_at", "09:30:00"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("starts_at", "09:30:00"),
    ]);
    let _ = &mut my_data;
}
