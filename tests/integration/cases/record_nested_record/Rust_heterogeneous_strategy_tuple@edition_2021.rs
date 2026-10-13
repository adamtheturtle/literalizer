#[allow(dead_code)]
#[derive(Clone)]
struct Record1 {
    name: &'static str,
    age: i32,
}
#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    id: i32,
    owner: Record1,
}
#[allow(non_snake_case)]
fn main() {
    let my_data = Record0 {
        id: 1,
        owner: Record1 {
            name: "Alice",
            age: 30,
        },
    };
    let _ = &my_data;
}
