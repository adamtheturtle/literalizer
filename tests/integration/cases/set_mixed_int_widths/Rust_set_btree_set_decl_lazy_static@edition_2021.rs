use std::sync::LazyLock;
use std::collections::BTreeSet;
fn main() {
    static my_data: LazyLock<BTreeSet<i64>> = LazyLock::new(|| BTreeSet::from([
        1,
        1099511627776i64,
    ]));
    let _ = my_data;
}
