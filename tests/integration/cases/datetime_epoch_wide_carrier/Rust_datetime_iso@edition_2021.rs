use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("within_i32", "2024-01-15T12:00:00"),
        ("beyond_i32", "2099-06-15T08:30:00"),
    ]);
    let _ = my_data;
}
