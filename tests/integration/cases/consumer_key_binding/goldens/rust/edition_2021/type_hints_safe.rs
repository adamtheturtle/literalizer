use std::collections::HashMap;
fn main() {
    let key_binding = HashMap::from([
        ("a", 1),
    ]);
    let _ = &key_binding;
}
