#[derive(Clone)]
pub struct Record1 {
    pub item: i32,
}
#[derive(Clone)]
pub struct Record2 {
    pub item: Option<()>,
}
#[derive(Clone)]
pub struct Record0 {
    pub integers: ((), (Record1,)),
    pub nulls: ((), (Record2,)),
    pub nested: (((), (Record1,)), ((Record1,), ())),
    pub reversed: ((Record1,), ()),
}
fn main() {
    let my_data = Record0 {
        integers: (
            (),
            (
                Record1 {
                    item: 1,
                },
            ),
        ),
        nulls: (
            (),
            (
                Record2 {
                    item: None::<()>,
                },
            ),
        ),
        nested: (
            (
                (),
                (
                    Record1 {
                        item: 2,
                    },
                ),
            ),
            (
                (
                    Record1 {
                        item: 3,
                    },
                ),
                (),
            ),
        ),
        reversed: (
            (
                Record1 {
                    item: 4,
                },
            ),
            (),
        ),
    };
    let _ = &my_data;
}
