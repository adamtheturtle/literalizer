fn main() {
    let my_data = vec![
        // strings stay data
        "https://example.org/a/*b*/",  // URL annotation
        "escaped quote: \" // still data",
        "backslash: \\",  // outside the string
        "/* not a comment */",
    ];
    let _ = &my_data;
}
