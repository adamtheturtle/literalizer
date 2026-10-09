pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn thing_go(_value: a) -> Nil { Nil }

pub fn main() {
  let item = GList([
    GInt(1),
    GInt(2),
  ])
  thing_go(item)
}
