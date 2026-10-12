use std::collections::HashMap;
fn main() {
    let std = HashMap::from([
        ("a", 1),
    ]);
    let arena = HashMap::from([
        ("a", 1),
    ]);
    let allocator = HashMap::from([
        ("a", 1),
    ]);
    let my_data = vec![
        std,
        arena,
        allocator,
    ];
    let _ = my_data;
}
