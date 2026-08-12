use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"x"#, "\0"),
        (r#"y"#, "\01"),
    ]);
    let _ = my_data;
}
