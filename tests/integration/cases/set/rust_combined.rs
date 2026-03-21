fn main() {
    {
        let my_data = HashSet::from(vec![
            "apple",
            "banana",
            "cherry",
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashSet::from(vec![
        "apple",
        "banana",
        "cherry",
    ]);
    let _ = my_data;
}
