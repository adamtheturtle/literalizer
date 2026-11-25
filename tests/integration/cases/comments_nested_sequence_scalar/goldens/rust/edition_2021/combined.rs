fn main() {
    let mut my_data = vec![
        vec!["ADD", "alice", "hello"],
        vec![
            "DEL",
            "bob",
            "5",  // removes "world"
        ],
    ];
    let _ = &my_data;
    my_data = vec![
        vec!["ADD", "alice", "hello"],
        vec![
            "DEL",
            "bob",
            "5",  // removes "world"
        ],
    ];
    let _ = &mut my_data;
}
