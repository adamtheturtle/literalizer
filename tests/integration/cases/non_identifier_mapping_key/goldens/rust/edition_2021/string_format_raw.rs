use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"not-a-field"#, 1),
    ]);
    let _ = &my_data;
}
