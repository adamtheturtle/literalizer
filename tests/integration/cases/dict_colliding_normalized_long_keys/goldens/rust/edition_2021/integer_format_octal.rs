use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a_b", 0o1),
        ("a-b", 0o2),
        ("averyveryverylongkeynamethatgoesonandonandon", 0o3),
        ("averyveryverylongkeynamethatgoesonandmore", 0o4),
    ]);
    let _ = &my_data;
}
