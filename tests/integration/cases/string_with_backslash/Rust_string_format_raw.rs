fn main() {
    let my_data = vec![
        r#"C:\path\to\file"#,
        r#"back\\slash"#,
        r#"hello \"world\""#,
        r##"path\to "# file"##,
        r#"trailing\"#,
        r#"both "quotes''' here"#,
    ];
    let _ = my_data;
}
