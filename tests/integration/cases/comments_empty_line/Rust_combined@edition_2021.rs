fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        "a",
        //
        "b",
    ];
    let _ = &my_data;
    my_data = vec![
        "a",
        //
        "b",
    ];
    let _ = &mut my_data;
}
