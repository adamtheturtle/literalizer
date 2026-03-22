fn main() {
    {
        let my_data = vec![
            vec![vec![1, 2], vec![3, 4]],
            vec![vec![5]],
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        vec![vec![1, 2], vec![3, 4]],
        vec![vec![5]],
    ];
    let _ = my_data;
}
