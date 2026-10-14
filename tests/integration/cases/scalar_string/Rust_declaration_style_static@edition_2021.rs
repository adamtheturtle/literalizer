fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: &str = "hello";
    let _ = &my_data;
}
