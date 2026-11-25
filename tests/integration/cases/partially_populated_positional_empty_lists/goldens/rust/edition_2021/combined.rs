fn main() {
    let mut my_data = vec![
        vec![Vec::new(), Vec::new()],
        vec![Vec::new(), vec![1]],
    ];
    let _ = &my_data;
    my_data = vec![
        vec![Vec::new(), Vec::new()],
        vec![Vec::new(), vec![1]],
    ];
    let _ = &mut my_data;
}
