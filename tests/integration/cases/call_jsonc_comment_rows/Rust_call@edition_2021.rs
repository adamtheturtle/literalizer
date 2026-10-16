fn main() {
    fn f<A, B>(_a: A, _b: B) {}
    // calls heading
    // before call one
    // first argument
    f(1, 2);  // after call one
    // second argument
    f(3, 4);
    // after all calls
}
