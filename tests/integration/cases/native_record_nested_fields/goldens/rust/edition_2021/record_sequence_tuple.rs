#[derive(Clone)]
pub struct Record1 {
    pub name: &'static str,
    pub active: bool,
}
#[derive(Clone)]
pub struct Record2 {
    pub name: &'static str,
    pub score: f64,
}
#[derive(Clone)]
pub struct Record0 {
    pub owner: Record1,
    pub members: (Record2, Record2),
}
fn main() {
    let my_data = Record0 {
        owner: Record1 {
            name: "Ada",
            active: false,
        },
        members: (
            Record2 {
                name: "Ada",
                score: 1.5,
            },
            Record2 {
                name: "Bob",
                score: 2.5,
            },
        ),
    };
    let _ = &my_data;
}
