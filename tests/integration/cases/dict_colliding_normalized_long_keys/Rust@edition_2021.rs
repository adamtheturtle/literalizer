use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a_b", 1),
        ("a-b", 2),
        ("averyveryverylongkeynamethatgoesonandonandon", 3),
        ("averyveryverylongkeynamethatgoesonandmore", 4),
    ]);
    let _ = my_data;
}
