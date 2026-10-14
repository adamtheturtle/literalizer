fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        "a",
        // trailing
    ];
    let _ = &my_data;
    my_data = vec![
        "a",
        // trailing
    ];
    let _ = &mut my_data;
}
