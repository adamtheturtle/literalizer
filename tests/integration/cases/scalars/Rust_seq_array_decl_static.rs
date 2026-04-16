fn main() {
    static my_data: [&str; 5] = [
        "42",
        "3.14",
        "True",
        "False",
        "hello \"world\"",
    ];
    let _ = my_data;
}
