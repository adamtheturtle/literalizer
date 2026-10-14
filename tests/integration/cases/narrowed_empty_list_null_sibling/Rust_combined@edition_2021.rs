fn main() {
    let mut my_data = vec![
        vec![None::<()>],
        vec![],
    ];
    let _ = &my_data;
    my_data = vec![
        vec![None::<()>],
        vec![],
    ];
    let _ = &mut my_data;
}
