use std::collections::HashMap;
fn main() {
    let text = "a\u{202A}b";
    let my_data = HashMap::from([
        ("value", text),
    ]);
    let _ = my_data;
}
