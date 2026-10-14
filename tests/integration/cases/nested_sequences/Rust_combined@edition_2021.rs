fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        vec![vec![1, 2], vec![3, 4]],
        vec![vec![5]],
    ];
    let _ = &my_data;
    my_data = vec![
        vec![vec![1, 2], vec![3, 4]],
        vec![vec![5]],
    ];
    let _ = &mut my_data;
}
