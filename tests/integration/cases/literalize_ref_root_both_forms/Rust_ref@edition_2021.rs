fn main() {
    let mut whole = vec![
        1,
        2,
    ];
    let _ = &mut whole;
    let mut my_data = whole.clone();
    let _ = &my_data;
    my_data = whole.clone();
    let _ = &mut my_data;
}
