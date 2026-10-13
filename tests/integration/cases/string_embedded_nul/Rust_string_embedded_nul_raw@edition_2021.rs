use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    let my_data = HashMap::from([
        (r#"x"#, "\0"),
        (r#"y"#, "\01"),
    ]);
    let _ = &my_data;
}
