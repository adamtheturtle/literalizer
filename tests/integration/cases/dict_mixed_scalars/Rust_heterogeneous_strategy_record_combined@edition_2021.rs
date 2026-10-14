#[allow(dead_code)]
#[derive(Clone)]
struct Record0 {
    a: i32,
    b: &'static str,
}
fn main() {
    #[allow(unused_mut)]
    let mut my_data = Record0 {
        a: 1,
        b: "x",
    };
    let _ = &my_data;
    my_data = Record0 {
        a: 1,
        b: "x",
    };
    let _ = &mut my_data;
}
