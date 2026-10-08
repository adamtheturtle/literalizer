struct Record0 {
    labels: [&'static str; 1],
}
fn main() {
    let first = Record0 {
        labels: [
            "owned",
        ],
    };
    let my_data = first;
    let _ = my_data;
}
