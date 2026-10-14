fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        None::<()>,
        None::<()>,
    ];
    let _ = &my_data;
    my_data = vec![
        None::<()>,
        None::<()>,
    ];
    let _ = &mut my_data;
}
