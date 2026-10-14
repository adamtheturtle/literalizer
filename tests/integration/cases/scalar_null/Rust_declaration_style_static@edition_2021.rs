fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: Option<()> = None::<()>;
    let _ = &my_data;
}
