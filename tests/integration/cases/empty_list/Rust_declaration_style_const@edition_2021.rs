#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    const my_data: [String; 0] = [] as [String; 0];
    let _ = &my_data;
}
