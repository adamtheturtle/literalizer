fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: [String; 0] = [] as [String; 0];
    let _ = &my_data;
}
