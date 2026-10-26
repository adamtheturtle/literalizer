fn main() {
    fn f<A>(_a: A) {}
    fn repr<A>(__arg: A) {}
    let ref_data = 1;
    repr(f(ref_data));
}
