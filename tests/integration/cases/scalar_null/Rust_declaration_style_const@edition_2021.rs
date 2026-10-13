#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    const my_data: Option<()> = None::<()>;
    let _ = &my_data;
}
