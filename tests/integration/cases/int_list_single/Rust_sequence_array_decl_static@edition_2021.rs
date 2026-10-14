fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: [i32; 1] = [
        1,
    ];
    let _ = &my_data;
}
