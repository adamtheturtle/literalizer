use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (0x1, "one"),
        (0x2, "two"),
        (0x2a, "answer"),
    ]);
    let _ = &my_data;
}
