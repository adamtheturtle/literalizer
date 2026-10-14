#[derive(Clone)]
pub struct Record1 {
    pub name: &'static str,
    pub age: i32,
}
#[derive(Clone)]
pub struct Record0 {
    pub id: i32,
    pub owner: Record1,
}
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
