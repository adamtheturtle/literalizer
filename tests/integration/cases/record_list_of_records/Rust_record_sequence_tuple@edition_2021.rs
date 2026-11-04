#[derive(Clone)]
pub struct Record1 {
    pub id: i32,
    pub label: &'static str,
}
#[derive(Clone)]
pub struct Record0 {
    pub name: &'static str,
    pub items: (Record1, Record1),
}
fn main() {
    let my_data = Record0 {
        name: "box",
        items: (
            Record1 {
                id: 1,
                label: "first",
            },
            Record1 {
                id: 2,
                label: "second",
            },
        ),
    };
    let _ = &my_data;
}
