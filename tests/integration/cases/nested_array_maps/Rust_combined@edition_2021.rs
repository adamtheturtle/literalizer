use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("groups", vec![vec![HashMap::from([("id", 1)])], vec![HashMap::from([("id", 2)])]]),
    ]);
    my_data = HashMap::from([
        ("groups", vec![vec![HashMap::from([("id", 1)])], vec![HashMap::from([("id", 2)])]]),
    ]);
    let _ = my_data;
}
