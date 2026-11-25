use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (0o1, "one"),
        (0o2, "two"),
        (0o52, "answer"),
    ]);
    let _ = &my_data;
}
