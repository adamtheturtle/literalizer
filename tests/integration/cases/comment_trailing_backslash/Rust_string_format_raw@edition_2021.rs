use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        // comment ending backslash \ .
        (r#"x"#, 1),
    ]);
    let _ = &my_data;
}
