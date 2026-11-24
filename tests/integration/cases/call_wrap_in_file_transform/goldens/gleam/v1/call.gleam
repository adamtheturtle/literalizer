pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_a: a, _b: b) -> Nil { Nil }

pub fn main() {
  let my_data = process(GInt(1), GInt(2))
  let _ = my_data
}
