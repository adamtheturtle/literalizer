fn main() {
    let mut my_data = vec![
        vec![Vec::<String>::new(), Vec::<String>::new()],
        vec![vec![1], vec![1]],
    ];
    let _ = &my_data;
    my_data = vec![
        vec![Vec::<String>::new(), Vec::<String>::new()],
        vec![vec![1], vec![1]],
    ];
    let _ = &mut my_data;
}
