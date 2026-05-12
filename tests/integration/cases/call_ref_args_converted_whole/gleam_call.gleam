pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn process(_data: a) -> Nil { Nil }

pub fn main() {
  let my_var = GList([
    GInt(1),
    GInt(2),
    GInt(3),
  ])
  process(my_var)
}
