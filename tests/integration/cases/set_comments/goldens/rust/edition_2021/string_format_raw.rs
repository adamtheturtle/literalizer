use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        r#"apple"#,  // inline comment
        // before banana
        r#"banana"#,
        // trailing
    ]);
    let _ = &my_data;
}
