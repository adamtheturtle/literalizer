// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    let _customRoot = r#"head
final my_data = 123;
final fakeRoot = 1;
final fixtureRoot = 1;
tail"#;
    let _ = &_customRoot;
}
