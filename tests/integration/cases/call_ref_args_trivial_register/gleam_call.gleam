pub type GVal {
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GList(List(GVal))
}
pub fn process(_value: a, _count: b) -> Nil { Nil }

pub fn main() {
  let my_int = GInt(1)
  let my_bool = GBool(True)
  let my_float = GFloat(3.14)
  let my_list = GList([
    GInt(1),
    GInt(2),
    GInt(3),
  ])
  process(my_int, GInt(42))
  process(my_bool, GInt(7))
  process(my_float, GInt(9))
  process(my_list, GInt(1))
}
