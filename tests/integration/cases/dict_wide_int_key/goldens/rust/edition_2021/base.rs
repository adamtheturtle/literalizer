use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (99999999999999999999999999i128, "tag"),
    ]);
    let _ = &my_data;
}
