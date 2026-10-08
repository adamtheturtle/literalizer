use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("missing", None::<()>),
    ]);
    let _ = my_data;
}
