fn main() {
    const my_data: (i32, f64, bool, bool, &str) = (
        42,
        3.14,
        true,
        false,
        "hello \"world\"",
    );
    let _ = my_data;
}
