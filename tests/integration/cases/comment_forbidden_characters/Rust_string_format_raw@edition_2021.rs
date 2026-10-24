use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"a"#, 1),  // tab	here and bidi <U+202E>after
        (r#"b"#, 2),
    ]);
    let _ = &my_data;
}
