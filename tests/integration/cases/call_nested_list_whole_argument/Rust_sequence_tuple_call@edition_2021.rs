fn main() {
    fn f<A>(_a: A) {}
    f(((1, 2), (3,)));
}
