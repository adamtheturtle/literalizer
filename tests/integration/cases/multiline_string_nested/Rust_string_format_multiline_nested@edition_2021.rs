use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"outer"#, vec![vec![r#"nested first line
  indented

nested last line
"#]]),
    ]);
    let _ = my_data;
}
