fn main() {
    fn f<A>(_a: A) {}
    f(vec![vec![1, 2], vec![3]]);
}
