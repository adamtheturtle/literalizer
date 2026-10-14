use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("starts_at", "09:30:00"),
    ]);
    let _ = &mut my_data;
}
