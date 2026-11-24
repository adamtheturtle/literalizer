use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"long_str"#, r#"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"#),
        (r#"quoted"#, r#"a"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"ba"b"#),
        (r#"wide"#, r#"中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中"#),
    ]);
    let _ = &my_data;
}
