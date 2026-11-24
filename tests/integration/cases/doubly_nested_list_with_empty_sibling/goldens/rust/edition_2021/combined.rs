fn main() {
    let mut my_data = vec![
        vec![vec![1, 2]],
        Vec::new(),
        vec![vec![3, 4]],
    ];
    let _ = &my_data;
    my_data = vec![
        vec![vec![1, 2]],
        Vec::new(),
        vec![vec![3, 4]],
    ];
    let _ = &mut my_data;
}
