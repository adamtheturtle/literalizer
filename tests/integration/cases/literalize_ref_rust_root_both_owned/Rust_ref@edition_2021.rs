fn main() {
    #[allow(unused_mut)]
    let mut shared = vec![
        1,
        2,
    ];
    #[allow(unused_mut)]
    let mut my_data = shared.clone();
    let _ = &my_data;
    my_data = shared.clone();
    let _ = &mut my_data;
}
