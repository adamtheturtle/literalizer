#[derive(Clone)]
pub struct Record0 {
    pub r#enum: i32,
    pub export: i32,
    pub given: i32,
    pub then: i32,
    pub r#as: i32,
    pub derives: i32,
    pub end: i32,
    pub extension: i32,
    pub infix: i32,
    pub inline: i32,
    pub opaque: i32,
    pub open: i32,
    pub transparent: i32,
    pub using: i32,
}
fn main() {
    let my_data = Record0 {
        r#enum: 1,
        export: 2,
        given: 3,
        then: 4,
        r#as: 5,
        derives: 6,
        end: 7,
        extension: 8,
        infix: 9,
        inline: 10,
        opaque: 11,
        open: 12,
        transparent: 13,
        using: 14,
    };
    let _ = &my_data;
}
