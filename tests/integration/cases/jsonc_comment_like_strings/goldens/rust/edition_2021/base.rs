fn main() {
    let my_data = vec![
        "// data",
        "/* data */",
        "escaped quote: \" // data",
        "backslash: \\",
    ];
    let _ = &my_data;
}
