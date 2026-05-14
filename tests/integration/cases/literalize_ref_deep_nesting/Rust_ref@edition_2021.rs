use std::collections::HashMap;
fn main() {
    let deep = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = HashMap::from([
        ("a", HashMap::from([("b", HashMap::from([("c", deep)]))])),
    ]);
    let _ = my_data;
}
