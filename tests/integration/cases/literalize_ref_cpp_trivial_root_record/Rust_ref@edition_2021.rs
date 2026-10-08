struct Record1 {
    value: i32,
}
struct Record0 {
    child: Record1,
}
fn main() {
    let first = Record0 {
        child: Record1 {
            value: 1,
        },
    };
    let my_data = first;
    let _ = my_data;
}
