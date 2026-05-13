use std::collections::HashSet;
fn main() {
    static my_data: HashSet<i64> = HashSet::from([
        1,
        1099511627776i64,
    ]);
    let _ = my_data;
}
