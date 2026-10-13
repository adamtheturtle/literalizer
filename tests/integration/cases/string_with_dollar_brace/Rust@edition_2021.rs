#[allow(non_snake_case)]
fn main() {
    let my_data = vec![
        "prefix ${HOME} suffix",
        "${interpolated}",
    ];
    let _ = &my_data;
}
