use std::collections::HashMap;
fn main() {
    let my_var = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = HashMap::from([
        ("key", my_var),
    ]);
    let _ = my_data;
}
