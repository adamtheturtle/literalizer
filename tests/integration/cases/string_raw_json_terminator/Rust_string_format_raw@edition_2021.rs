use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#")json"#, r#"x"#),
    ]);
    let _ = &my_data;
}
