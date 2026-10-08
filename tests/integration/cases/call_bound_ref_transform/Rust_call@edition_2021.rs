fn main() {
    fn f<A>(_a: A) {}
    let ref_data = 1;
    f(ref_data);
}
