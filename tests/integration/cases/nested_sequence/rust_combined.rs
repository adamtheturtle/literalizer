fn main() {
    {
        let my_data = vec![
            true,
            "hi",
            vec![1, 2],
            None::<()>,
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        true,
        "hi",
        vec![1, 2],
        None::<()>,
    ];
    let _ = my_data;
}
