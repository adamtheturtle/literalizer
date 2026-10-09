fn main() {
    fn f<A>(_value: A) {}
    let ref_data = vec![
        1,
        2,
    ];
    f(vec![
        ref_data,
    ]);
    f(vec![
        ref_data,
    ]);
}
