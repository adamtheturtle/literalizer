use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("double", "a b"),
        ("single", "c d"),
        ("both", "e f g"),
        ("continued", "hi"),
        ("escaped backslash", "j\\ k"),
    ]);
    let _ = my_data;
}
