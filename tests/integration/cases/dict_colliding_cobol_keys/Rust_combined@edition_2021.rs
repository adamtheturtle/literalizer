use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("user_name", 1),
        ("user.name", 2),
        ("user-name", 3),
        ("field_name_that_is_really_quite_long_one", 4),
        ("field_name_that_is_really_quite_long_two", 5),
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("user_name", 1),
        ("user.name", 2),
        ("user-name", 3),
        ("field_name_that_is_really_quite_long_one", 4),
        ("field_name_that_is_really_quite_long_two", 5),
    ]);
    let _ = &mut my_data;
}
