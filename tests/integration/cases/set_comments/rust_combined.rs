fn main() {
    {
        let my_data = HashSet::from(vec![
            "apple",  // inline comment
            // before banana
            "banana",
            // trailing
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashSet::from(vec![
        "apple",  // inline comment
        // before banana
        "banana",
        // trailing
    ]);
    let _ = my_data;
}
