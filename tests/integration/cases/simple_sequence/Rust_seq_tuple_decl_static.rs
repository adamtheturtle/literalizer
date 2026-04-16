fn main() {
    static my_data: (i32, &str, bool, Option<()>) = (
        1,
        "hello",
        true,
        None::<()>,
    );
    let _ = my_data;
}
