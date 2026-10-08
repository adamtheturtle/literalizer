use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"x"#, "line1\r\nline2"),
    ]);
    let _ = my_data;
}
