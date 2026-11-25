use std::collections::HashMap;
fn main() {
    let shared_time = "12:30:15+02:00";
    let my_data = HashMap::from([
        ("x", shared_time),
    ]);
    let _ = &my_data;
}
