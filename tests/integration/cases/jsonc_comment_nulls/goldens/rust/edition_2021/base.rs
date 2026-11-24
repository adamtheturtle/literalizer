use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        // null heading
        // before null
        ("a", None::<()>),  // first null
        ("b", None::<()>),  // second null
    ]);
    let _ = &my_data;
}
