fn main() {
    let mut my_data = vec![
        None::<()>,
    ];
    let _ = &my_data;
    my_data = vec![
        None::<()>,
    ];
    let _ = &mut my_data;
}
