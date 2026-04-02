fn main() {
    let mut my_data = vec![
        "prefix ${HOME} suffix",
        "${interpolated}",
    ];
    my_data = vec![
        "prefix ${HOME} suffix",
        "${interpolated}",
    ];
    let _ = my_data;
}
