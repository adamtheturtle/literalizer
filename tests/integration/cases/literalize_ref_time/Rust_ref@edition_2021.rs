use std::collections::HashMap;
fn main() {
    let my_time = "01:02:03";
    let my_data = HashMap::from([
        ("x", my_time),
    ]);
    let _ = my_data;
}
