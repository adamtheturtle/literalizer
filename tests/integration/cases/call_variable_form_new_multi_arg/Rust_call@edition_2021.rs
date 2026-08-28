fn main() {
    fn record_entry<A, B, C>(_s: A, _n: B, _b: C) {}
    let my_data = record_entry("a", 1, true);
    let _ = my_data;
}
