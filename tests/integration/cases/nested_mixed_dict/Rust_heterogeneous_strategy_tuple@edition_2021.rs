#[allow(dead_code)]
#[derive(Clone)]
struct Record1 {
    a: i32,
    b: &'static str,
    c: Option<()>,
}
#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    outer: Record1,
}
#[allow(non_snake_case)]
fn main() {
    let my_data = Record0 {
        outer: Record1 {
            a: 1,
            b: "x",
            c: None::<()>,
        },
    };
    let _ = &my_data;
}
