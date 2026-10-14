fn main() {
    let mut my_data = vec![
        "café",
        "中文",
        "😀",
    ];
    let _ = &my_data;
    my_data = vec![
        "café",
        "中文",
        "😀",
    ];
    let _ = &mut my_data;
}
