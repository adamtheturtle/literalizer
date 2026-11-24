use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (r#"fffe"#, r#"￾"#),
        (r#"ffff"#, r#"￿"#),
    ]);
    let _ = &my_data;
}
