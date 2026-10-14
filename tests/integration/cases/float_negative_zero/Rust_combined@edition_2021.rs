fn main() {
    let mut my_data = vec![
        -0.0,
        1.5,
    ];
    let _ = &my_data;
    my_data = vec![
        -0.0,
        1.5,
    ];
    let _ = &mut my_data;
}
