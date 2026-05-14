use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        ("a", None::<()>),
        ("b", None::<()>),
        // trailing
    ]);
    my_data = HashMap::from([
        ("a", None::<()>),
        ("b", None::<()>),
        // trailing
    ]);
    let _ = my_data;
}
