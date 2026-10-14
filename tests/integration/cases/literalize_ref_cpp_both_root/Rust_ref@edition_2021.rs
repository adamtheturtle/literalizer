fn main() {
    let mut shared = vec![
        1,
        2,
    ];
    let mut my_data = shared.clone();
    let _ = &my_data;
    my_data = shared.clone();
    let _ = &mut my_data;
    let _ = &mut shared;
}
