use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("test", (5, ("compile", "test"))),
        ("package", (7, ("link", "test"))),
    ]);
    let _ = my_data;
}
