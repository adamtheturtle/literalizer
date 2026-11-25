use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a_b", 0x1),
        ("a-b", 0x2),
        ("averyveryverylongkeynamethatgoesonandonandon", 0x3),
        ("averyveryverylongkeynamethatgoesonandmore", 0x4),
    ]);
    let _ = &my_data;
}
