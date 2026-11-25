use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        // server
        (r#"host"#, r#"localhost"#),  // default
    ]);
    let _ = &my_data;
}
