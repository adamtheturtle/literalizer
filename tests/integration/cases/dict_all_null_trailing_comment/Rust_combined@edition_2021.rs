use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("a", None::<()>),
        ("b", None::<()>),
        // trailing
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("a", None::<()>),
        ("b", None::<()>),
        // trailing
    ]);
    let _ = &mut my_data;
}
