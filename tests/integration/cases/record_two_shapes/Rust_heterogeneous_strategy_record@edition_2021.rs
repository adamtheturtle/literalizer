use std::collections::HashMap;
struct Record1 {
    count: i32,
    rate: i32,
}
struct Record2 {
    retries: i32,
    timeout: i32,
}
struct Record0 {
    metrics: Record1,
    flags: Record2,
}
fn main() {
    let my_data = Record0 {
        metrics: Record1 {
            count: 100,
            rate: 50,
        },
        flags: Record2 {
            retries: 3,
            timeout: 30,
        },
    };
    let _ = my_data;
}
