use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"_"#, HashMap::from([(r#"a"#, 1), (r#"b"#, 2)])),
    ]);
    let _ = &my_data;
}
