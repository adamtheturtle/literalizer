fn main() {
    fn f<A, B>(_a: A, _b: B) {}
    f(2, "hello");  // trailing note
    // next element
    f(3, "world");
}
