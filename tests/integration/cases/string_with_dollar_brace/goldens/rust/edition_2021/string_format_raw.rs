fn main() {
    let my_data = vec![
        r#"prefix ${HOME} suffix"#,
        r#"${interpolated}"#,
    ];
    let _ = &my_data;
}
