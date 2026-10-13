#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        "C:\\path\\to\\file",
        "back\\\\slash",
        "hello \\\"world\\\"",
        "path\\to \"# file",
        "trailing\\",
        "both \"quotes''' here",
        "line1\\nline2\nwith newline",
    ];
    let _ = &my_data;
    my_data = vec![
        "C:\\path\\to\\file",
        "back\\\\slash",
        "hello \\\"world\\\"",
        "path\\to \"# file",
        "trailing\\",
        "both \"quotes''' here",
        "line1\\nline2\nwith newline",
    ];
    let _ = &mut my_data;
}
