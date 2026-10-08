use std::collections::HashMap;
fn main() {
    let external_value = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = vec![
        external_value,
    ];
    let _ = my_data;
}
