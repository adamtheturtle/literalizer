fn main() {
    #[allow(non_upper_case_globals)]
    const my_data: i32 = 42;
    let _ = &my_data;
}
