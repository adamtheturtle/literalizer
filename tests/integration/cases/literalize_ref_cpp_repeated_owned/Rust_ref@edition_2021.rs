fn main() {
    let shared = vec![
        1,
        2,
    ];
    let my_data = vec![
        shared.clone(),
        shared.clone(),
    ];
    let _ = my_data;
}
