struct Record0 {
    r#type: &'static str,
    r#match: &'static str,
    error: &'static str,
    switch: &'static str,
    class: &'static str,
    inout: &'static str,
    int: &'static str,
    new: &'static str,
    r#static: &'static str,
    fun: &'static str,
    object: &'static str,
    val: &'static str,
    when: &'static str,
    func: &'static str,
    r#let: &'static str,
    var: &'static str,
    template: &'static str,
    id: i32,
}
fn main() {
    let my_data = vec![
        Record0 { r#type: "a", r#match: "b", error: "c", switch: "d", class: "e", inout: "ee", int: "f", new: "g", r#static: "h", fun: "i", object: "j", val: "k", when: "l", func: "m", r#let: "n", var: "o", template: "p", id: 1 },
    ];
    let _ = my_data;
}
