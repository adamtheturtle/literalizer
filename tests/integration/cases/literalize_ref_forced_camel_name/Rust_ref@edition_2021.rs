use std::collections::HashMap;
fn main() {
    let user_obj = HashMap::from([
        ("_", "_"),
    ]);
    let my_data = user_obj;
    let _ = &my_data;
}
