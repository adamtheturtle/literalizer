use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"08"#, r#"value"#),
    ]);
    let _ = &my_data;
}
