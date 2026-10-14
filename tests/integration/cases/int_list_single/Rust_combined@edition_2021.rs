fn main() {
    let mut my_data = vec![
        1,
    ];
    let _ = &my_data;
    my_data = vec![
        1,
    ];
    let _ = &mut my_data;
}
