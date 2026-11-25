use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"key"#, r#"it's here"#),  // a comment
    ]);
    let _ = &my_data;
}
