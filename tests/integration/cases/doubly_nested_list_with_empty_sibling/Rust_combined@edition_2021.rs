fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        vec![vec![1, 2]],
        vec![],
        vec![vec![3, 4]],
    ];
    let _ = &my_data;
    my_data = vec![
        vec![vec![1, 2]],
        vec![],
        vec![vec![3, 4]],
    ];
    let _ = &mut my_data;
}
