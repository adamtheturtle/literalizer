use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"name"#, r#"Alice"#),
        (r#"age"#, r#"30"#),
        (r#"active"#, r#"True"#),
        (r#"score"#, r#"None"#),
    ]);
    let _ = my_data;
}
