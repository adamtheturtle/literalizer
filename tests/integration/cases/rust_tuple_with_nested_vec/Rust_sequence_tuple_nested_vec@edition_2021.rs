use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("lint", (2, Vec::<&str>::new())),
        ("test", (5, vec!["compile"])),
        ("package", (7, vec!["link", "test"])),
    ]);
    let _ = my_data;
}
