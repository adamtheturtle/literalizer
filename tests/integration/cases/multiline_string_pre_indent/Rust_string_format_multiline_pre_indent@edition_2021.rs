
fn main() {
    let my_data = r#"
first line
  indented

last line
"#;
    assert_eq!(my_data, "\nfirst line\n  indented\n\nlast line\n");
}
