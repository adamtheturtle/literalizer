fn main() {
    fn f<A>(_a: A) {}
    f([] as [String; 0]);
}
