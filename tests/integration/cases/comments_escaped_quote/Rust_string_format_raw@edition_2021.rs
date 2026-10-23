use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"key"#, r#"value " # not a comment"#),  // real
    ]);
    let _ = &my_data;
}
