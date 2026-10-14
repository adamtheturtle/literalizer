fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        true,
        false,
        true,
    ];
    let _ = &my_data;
    my_data = vec![
        true,
        false,
        true,
    ];
    let _ = &mut my_data;
}
