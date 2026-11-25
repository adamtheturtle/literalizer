#[derive(Clone)]
pub struct Record1 {
    pub count: i32,
    pub rate: i32,
}
#[derive(Clone)]
pub struct Record2 {
    pub retries: i32,
    pub timeout: i32,
}
#[derive(Clone)]
pub struct Record0 {
    pub metrics: Record1,
    pub flags: Record2,
}
fn main() {
    let my_data = Record0 {
        metrics: Record1 {
            count: 100,
            rate: 50,
        },
        flags: Record2 {
            retries: 3,
            timeout: 30,
        },
    };
    let _ = &my_data;
}
