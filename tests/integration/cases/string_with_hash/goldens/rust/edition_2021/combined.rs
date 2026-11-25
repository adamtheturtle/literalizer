fn main() {
    let mut my_data = vec![
        "issue #{42}",
        "color #red",
    ];
    let _ = &my_data;
    my_data = vec![
        "issue #{42}",
        "color #red",
    ];
    let _ = &mut my_data;
}
