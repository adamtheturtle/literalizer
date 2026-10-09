#[derive(Clone)]
struct Record1 {
    x: &'static str,
}
#[derive(Clone)]
struct Record2 {
    x: i32,
}
#[derive(Clone)]
struct Record0 {
    direct: Record1,
    bound: Record2,
}
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
    let _ = my_data;
}
