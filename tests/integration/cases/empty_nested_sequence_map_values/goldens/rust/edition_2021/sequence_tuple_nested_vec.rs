use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("alpha", (2, Vec::<&str>::new())),
        ("beta", (5, vec!["x"])),
    ]);
    let _ = &my_data;
}
