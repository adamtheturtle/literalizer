use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("cr", "a\rb"),
        ("crlf", "a\r\nb"),
        ("lf", "a\nb"),
    ]);
    let _ = my_data;
}
