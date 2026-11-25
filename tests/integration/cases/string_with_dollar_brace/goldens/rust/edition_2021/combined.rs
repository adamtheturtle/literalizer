fn main() {
    let mut my_data = vec![
        "prefix ${HOME} suffix",
        "${interpolated}",
    ];
    let _ = &my_data;
    my_data = vec![
        "prefix ${HOME} suffix",
        "${interpolated}",
    ];
    let _ = &mut my_data;
}
