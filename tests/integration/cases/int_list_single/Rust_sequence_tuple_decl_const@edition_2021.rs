fn main() {
    #[allow(non_upper_case_globals)]
    const my_data: (i32,) = (
        1,
    );
    let _ = &my_data;
}
