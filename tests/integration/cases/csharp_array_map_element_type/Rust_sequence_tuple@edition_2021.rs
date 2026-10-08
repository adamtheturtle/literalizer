use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("d", (HashMap::from([("a", (HashMap::from([("b", (1, (2.5, ("x", (true,)))))]),))]),)),
    ]);
    let _ = my_data;
}
