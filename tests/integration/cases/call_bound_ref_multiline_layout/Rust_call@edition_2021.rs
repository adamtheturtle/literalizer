fn main() {
    fn f<A>(_value: A) {}
    let x = vec![
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
            x,
        ],
    ]);
}
