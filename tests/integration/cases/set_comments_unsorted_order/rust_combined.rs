fn main() {
    {
        let my_data = HashSet::from(vec![
            // before apple
            "apple",
            "banana",  // banana inline
            // trailing
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashSet::from(vec![
        // before apple
        "apple",
        "banana",  // banana inline
        // trailing
    ]);
    let _ = my_data;
}
