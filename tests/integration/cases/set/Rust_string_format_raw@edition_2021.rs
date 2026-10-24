use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        r#"apple"#,
        r#"banana"#,
        r#"cherry"#,
    ]);
    let _ = &my_data;
}
