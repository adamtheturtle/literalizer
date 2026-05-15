use std::collections::HashMap;
struct Record1 {
    name: &'static str,
    age: i32,
}
struct Record0 {
    id: i32,
    owner: Record1,
}
fn main() {
    let my_data = Record0 {
        id: 1,
        owner: Record1 {
            name: "Alice",
            age: 30,
        },
    };
    let _ = my_data;
}
