fn main() {
    let my_data = vec![
        r#"first line
  indented

last line"#,
        r#"
leading newline"#,
        r#"trailing newline
"#,
        r#"
leading and trailing
"#,
        r#"quotes: """ ''' ` and backslash: \"#,
        r#"interpolation: ${value} #{value} #@value #$value $value"#,
        r#"backslash before newline: \
next line"#,
        "trailing spaces  \nnext",
        r#"C++ delimiter collision: )LITERALIZER"
value"#,
        r##"Rust delimiter collision: "#
value"##,
        r#"Lua delimiter collision: ]]
value"#,
        "Ruby fallback interpolation  \n#{expression} #@instance #$global",
        "NUL followed by a digit: \07",
        "carriage\rreturn",
    ];
    let _ = my_data;
}
