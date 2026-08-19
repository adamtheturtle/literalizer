use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"v"#, "a\u{202A}\u{202B}\u{202C}\u{202D}\u{202E}\u{2066}\u{2067}\u{2068}\u{2069}b"),
    ]);
    let _ = my_data;
}
