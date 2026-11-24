#[derive(Clone)]
pub struct Record0 {
    pub r#type: &'static str,
    pub r#match: &'static str,
    pub error: &'static str,
    pub switch: &'static str,
    pub class: &'static str,
    pub inout: &'static str,
    pub int: &'static str,
    pub new: &'static str,
    pub r#static: &'static str,
    pub fun: &'static str,
    pub object: &'static str,
    pub val: &'static str,
    pub when: &'static str,
    pub func: &'static str,
    pub r#let: &'static str,
    pub var: &'static str,
    pub template: &'static str,
    pub id: i32,
}
fn main() {
    let my_data = vec![
        Record0 { r#type: "a", r#match: "b", error: "c", switch: "d", class: "e", inout: "ee", int: "f", new: "g", r#static: "h", fun: "i", object: "j", val: "k", when: "l", func: "m", r#let: "n", var: "o", template: "p", id: 1 },
    ];
    let _ = &my_data;
}
