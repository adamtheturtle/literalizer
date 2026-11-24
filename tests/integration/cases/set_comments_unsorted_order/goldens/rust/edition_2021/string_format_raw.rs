use std::collections::HashSet;
fn main() {
    let my_data = HashSet::from([
        // before apple
        r#"apple"#,
        r#"banana"#,  // banana inline
        // trailing
    ]);
    let _ = &my_data;
}
