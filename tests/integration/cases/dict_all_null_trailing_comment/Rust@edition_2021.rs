use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        ("a", None::<()>),
        ("b", None::<()>),
        // trailing
    ]);
    let _ = &my_data;
}
