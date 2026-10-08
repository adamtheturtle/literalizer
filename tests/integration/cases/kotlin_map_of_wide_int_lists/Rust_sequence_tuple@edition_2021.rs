use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", (4294967296i64, 4294967297i64)),
    ]);
    let _ = my_data;
}
