use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a_b", 0b1),
        ("a-b", 0b10),
        ("averyveryverylongkeynamethatgoesonandonandon", 0b11),
        ("averyveryverylongkeynamethatgoesonandmore", 0b100),
    ]);
    let _ = &my_data;
}
