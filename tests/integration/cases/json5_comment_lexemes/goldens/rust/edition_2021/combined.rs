use std::collections::HashMap;
fn main() {
    let mut my_data = HashMap::from([
        // heading
        ("a", "single ' // data"),
        ("b", "linecontinuation"),
        ("c", "\\"),  // actual comment
        ("d", "  "),  // final comment
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        // heading
        ("a", "single ' // data"),
        ("b", "linecontinuation"),
        ("c", "\\"),  // actual comment
        ("d", "  "),  // final comment
    ]);
    let _ = &mut my_data;
}
