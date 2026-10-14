fn main() {
    #[allow(unused_mut)]
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
