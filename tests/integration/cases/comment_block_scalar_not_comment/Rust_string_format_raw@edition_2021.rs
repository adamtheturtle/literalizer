use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"description"#, "# not a comment\n"),
        (r#"name"#, r#"foo"#),
    ]);
    let _ = &my_data;
}
