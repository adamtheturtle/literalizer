use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("description", "# not a comment\n"),
        ("name", "foo"),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("description", "# not a comment\n"),
        ("name", "foo"),
    ]);
    let _ = &mut my_data;
}
