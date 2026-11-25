use std::collections::BTreeMap;
fn main() {
    let my_data = BTreeMap::from([
        ("morning", "09:30:00"),
        ("afternoon", "14:15:00"),
        ("evening", "23:59:59"),
    ]);
    let _ = &my_data;
}
