fn main() {
    let my_null = None::<()>;
    let my_data = vec![
        my_null,
        None::<()>,
    ];
    let _ = my_data;
}
