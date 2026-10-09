struct Record1 {
    x: i32,
    y: Option<()>,
}
struct Record2 {
    x: Option<()>,
    y: Option<()>,
}
struct Record3 {
    x: i32,
    y: i32,
}
struct Record0 {
    nullable: Record1,
    null_fields: Record2,
    plain: Record3,
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
    let _ = my_data;
}
