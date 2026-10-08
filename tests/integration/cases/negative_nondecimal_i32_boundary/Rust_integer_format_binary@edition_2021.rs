use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("minimum", -0b10000000000000000000000000000000),
        ("below", -0b10110010110100000101111000000000i64),
    ]);
    let _ = my_data;
}
