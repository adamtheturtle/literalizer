pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn foo_class(_value: a) -> Nil { Nil }

pub fn main() {
  foo_class(GInt(1))
}
