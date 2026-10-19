use std::collections::HashMap;
fn main() {
    let allocator = HashMap::from([
        ("a", 1),
    ]);
    let _ = &allocator;
}
