fn main() {
    fn f<A>(_value: A) {}
    let ref_data = vec![
        vec![
            1,
            2,
        ],
        vec![
            3,
            4,
        ],
    ];
    f(vec![
        vec![
            ref_data,
        ],
    ]);
}
