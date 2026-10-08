use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"cr"#, "a\rb"),
        (r#"crlf"#, "a\r\nb"),
        (r#"lf"#, "a\nb"),
    ]);
    let _ = my_data;
}
