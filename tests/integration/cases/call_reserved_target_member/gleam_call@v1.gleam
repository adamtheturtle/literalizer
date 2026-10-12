pub type GVal {
  GInt(Int)
}
pub fn obj_class(_a: a) -> Nil { Nil }

pub fn main() {
  obj_class(GInt(42))
}
