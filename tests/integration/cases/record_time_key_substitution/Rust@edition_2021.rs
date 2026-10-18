use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("value", HashMap::from([("01:02:03", 1)])),
    ]);
    let _ = &my_data;
}
