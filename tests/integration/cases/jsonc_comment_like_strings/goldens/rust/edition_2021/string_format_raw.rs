fn main() {
    let my_data = vec![
        r#"// data"#,
        r#"/* data */"#,
        r#"escaped quote: " // data"#,
        r#"backslash: \"#,
    ];
    let _ = &my_data;
}
