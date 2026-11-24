use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("quote\"backslash\\", 1),
        ("line\nbreak", 2),
        ("$(literal)${text}", 3),
        ("RStr prefix", 4),
    ]);
    let _ = &my_data;
}
