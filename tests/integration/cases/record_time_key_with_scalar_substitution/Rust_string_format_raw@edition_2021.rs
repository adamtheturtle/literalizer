use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"value"#, None::<()>),
        (r#"other"#, None::<()>),
    ]);
    let _ = &my_data;
}
