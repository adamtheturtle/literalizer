fn main() {
    #[allow(unused_mut)]
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
