use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("fffe", "￾"),
        ("ffff", "￿"),
    ]);
    let _ = &my_data;
}
