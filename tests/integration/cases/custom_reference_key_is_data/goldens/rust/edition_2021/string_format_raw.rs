use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"reference"#, r#"whole"#),
    ]);
    let _ = &my_data;
}
