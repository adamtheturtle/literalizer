#[derive(Clone)]
pub struct Record1 {
    pub x: i32,
    pub y: Option<()>,
}
#[derive(Clone)]
pub struct Record2 {
    pub x: Option<()>,
    pub y: Option<()>,
}
#[derive(Clone)]
pub struct Record3 {
    pub x: i32,
    pub y: i32,
}
#[derive(Clone)]
pub struct Record0 {
    pub nullable: Record1,
    pub null_fields: Record2,
    pub plain: Record3,
}
fn main() {
    let nullable = Record1 {
        x: 1,
        y: None::<()>,
    };
    let null_fields = Record2 {
        x: None::<()>,
        y: None::<()>,
    };
    let plain = Record3 {
        x: 1,
        y: 2,
    };
    let my_data = Record0 {
        nullable: nullable,
        null_fields: null_fields,
        plain: plain,
    };
    let _ = &my_data;
}
