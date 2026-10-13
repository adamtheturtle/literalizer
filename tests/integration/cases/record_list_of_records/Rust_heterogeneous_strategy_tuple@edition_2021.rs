#[allow(dead_code)]
#[derive(Clone)]
struct Record1 {
    id: i32,
    label: &'static str,
}
#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    name: &'static str,
    items: Vec<Record1>,
}
#[allow(non_snake_case)]
fn main() {
    let my_data = Record0 {
        name: "box",
        items: vec![
            Record1 {
                id: 1,
                label: "first",
            },
            Record1 {
                id: 2,
                label: "second",
            },
        ],
    };
    let _ = &my_data;
}
