fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: bool = true;
    let _ = &my_data;
}
