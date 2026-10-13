use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_var = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = my_var;
    let _ = &my_data;
}
