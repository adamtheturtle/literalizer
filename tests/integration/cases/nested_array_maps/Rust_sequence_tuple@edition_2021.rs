use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("groups", ((HashMap::from([("id", 1)]),), (HashMap::from([("id", 2)]),))),
    ]);
    let _ = my_data;
}
