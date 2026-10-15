fn main() {
    let mut my_data = vec![
        vec![None::<()>],
        Vec::new(),
    ];
    let _ = &my_data;
    my_data = vec![
        vec![None::<()>],
        Vec::new(),
    ];
    let _ = &mut my_data;
}
