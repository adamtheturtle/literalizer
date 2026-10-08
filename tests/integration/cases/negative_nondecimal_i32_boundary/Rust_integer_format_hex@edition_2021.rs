use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("minimum", -0x80000000),
        ("below", -0xb2d05e00i64),
    ]);
    let _ = my_data;
}
