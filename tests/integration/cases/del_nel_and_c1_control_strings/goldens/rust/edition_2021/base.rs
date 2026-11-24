use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("del", "ab"),
        ("nel", "ab"),
        ("c1", "ab"),
    ]);
    let _ = &my_data;
}
