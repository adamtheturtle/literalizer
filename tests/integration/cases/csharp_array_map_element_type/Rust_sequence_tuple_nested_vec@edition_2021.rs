use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("d", vec![HashMap::from([("a", vec![HashMap::from([("b", (1, (2.5, ("x", vec![true]))))])])])]),
    ]);
    let _ = my_data;
}
