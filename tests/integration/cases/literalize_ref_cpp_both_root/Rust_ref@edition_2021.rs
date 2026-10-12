fn main() {
    let mut shared = vec![
        1,
        2,
    ];
    let mut my_data = shared.clone();
    my_data = shared.clone();
    let _ = my_data;
}
