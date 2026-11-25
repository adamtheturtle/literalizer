use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (0b1, "one"),
        (0b10, "two"),
        (0b101010, "answer"),
    ]);
    let _ = &my_data;
}
