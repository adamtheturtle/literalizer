fn main() {
    let shared = (
        1,
        "x",
    );
    let my_data = (
        shared,
        shared,
    );
    let _ = my_data;
}
