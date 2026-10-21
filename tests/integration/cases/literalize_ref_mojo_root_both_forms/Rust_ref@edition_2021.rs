fn main() {
    let mut whole = vec![
        1,
        2,
    ];
    let mut my_data = whole.clone();
    let _ = &my_data;
    my_data = whole.clone();
    let _ = &mut my_data;
    let _ = &mut whole;
}
