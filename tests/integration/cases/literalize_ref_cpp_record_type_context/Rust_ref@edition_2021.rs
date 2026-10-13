#[allow(dead_code)]
#[derive(Clone)]
struct Record1 {
    x: &'static str,
}
#[allow(dead_code)]
#[derive(Clone)]
struct Record2 {
    x: i32,
}
#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    direct: Record1,
    bound: Record2,
}
#[allow(non_snake_case)]
fn main() {
    let first = Record2 {
        x: 1,
    };
    let my_data = Record0 {
        direct: Record1 {
            x: "s",
        },
        bound: first,
    };
    let _ = &my_data;
}
