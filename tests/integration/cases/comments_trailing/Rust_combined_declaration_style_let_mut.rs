fn main() {
    {
        let mut my_data = vec![
            "a",
            // trailing
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        "a",
        // trailing
    ];
    let _ = my_data;
}
