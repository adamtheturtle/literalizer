#[derive(Clone)]
pub struct Record1 {
    pub values: [i32; 2],
}
#[derive(Clone)]
pub struct Record2 {
    pub nested: [[i32; 2]; 2],
}
#[derive(Clone)]
pub struct Record0 {
    pub trivial: Record1,
    pub nested: Record2,
}
fn main() {
    let trivial = Record1 {
        values: [
            1,
            2,
        ],
    };
    let nested = Record2 {
        nested: [
            [
                1,
                2,
            ],
            [
                3,
                4,
            ],
        ],
    };
    let my_data = Record0 {
        trivial: trivial,
        nested: nested,
    };
    let _ = &my_data;
}
