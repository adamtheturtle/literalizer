use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"message"#, r#"no comment here"#),
    ]);
    let _ = &my_data;
}
