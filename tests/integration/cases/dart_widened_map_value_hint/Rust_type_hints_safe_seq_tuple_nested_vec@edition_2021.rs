use std::collections::HashMap;
fn main() {
    let my_data = (
        HashMap::from([
            ("a", 1),
        ]),
        1,
        "x",
        true,
        2.5,
        None::<()>,
    );
    let _ = my_data;
}
