use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let val_x = HashMap::from([
        ("_", "_"),
    ]);
    let val_y = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = vec![
        val_x,
        val_y,
    ];
    let _ = &my_data;
}
