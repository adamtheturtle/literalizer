use std::collections::HashMap;
struct Record0 {
    x: i32,
}
struct Record1 {
    x: &'static str,
}
struct Record2 {
    x: i32,
}
struct Record0 {
    direct: Record1,
    bound: Record2,
}
fn main() {
    let first = Record2 {
        x: 1,
    };
    let my_data = HashMap::from([
        ("direct", HashMap::from([("x", "s")])),
        ("bound", first),
    ]);
    let _ = my_data;
}
