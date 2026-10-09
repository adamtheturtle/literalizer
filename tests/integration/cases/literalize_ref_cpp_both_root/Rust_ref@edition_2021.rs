fn main() {
    let mut shared = vec![
        1,
        2,
    ];
    let mut my_data = shared;
    my_data = shared;
    let _ = my_data;
}
