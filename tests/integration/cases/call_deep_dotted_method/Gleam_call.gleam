pub type GVal {
  GNull
  GBool(Bool)
  GInt(Int)
  GFloat(Float)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
  GSet(List(GVal))
}
pub fn obj_api_client_post(_data: a) -> Nil { panic }

pub fn main() {
  obj_api_client_post(GStr("hello"))
  obj_api_client_post(GInt(42))
  obj_api_client_post(GBool(True))
}
