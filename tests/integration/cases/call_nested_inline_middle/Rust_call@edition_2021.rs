fn main() {
    fn f<A>(_ops: A) {}
    f(vec![vec!["DEL", "b", "10"], vec!["ADD", "a", "x"]]);  // note
}
