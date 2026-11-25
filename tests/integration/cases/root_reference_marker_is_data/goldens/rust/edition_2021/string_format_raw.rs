use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"$ref"#, r#"schema.json"#),
    ]);
    let _ = &my_data;
}
