fn main() {
    let value = None::<()>;
    let my_data = vec![
        value,
        value,
        None::<()>,
    ];
    let _ = &my_data;
}
