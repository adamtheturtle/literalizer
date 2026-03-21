fn main() {
    let _ = HashMap::from(vec![
        ("key\nwith\nnewlines", "value1"),
        ("key\twith\ttabs", "value2"),
        ("", "value3"),
    ]);
}
