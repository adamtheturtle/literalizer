use std::collections::HashMap;
fn main() {
    let shared_var = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = vec![
        shared_var,
        shared_var,
    ];
    let _ = my_data;
}
