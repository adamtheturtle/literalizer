use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"v"#, "a\u{202A}\0é😀b"),
    ]);
    let _ = my_data;
}
