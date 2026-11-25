use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"key"#, r#""bang!""#),  // real
    ]);
    let _ = &my_data;
}
