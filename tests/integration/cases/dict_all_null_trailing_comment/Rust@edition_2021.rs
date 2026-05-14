use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("a", None::<()>),
        ("b", None::<()>),
        // trailing
    ]);
    let _ = my_data;
}
