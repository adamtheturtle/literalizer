fn main() {
    fn f<A, B>(_a: A, _b: B) {}
    f(2, "hello");  // trailing note
    f(3, "world");  // another note
}
