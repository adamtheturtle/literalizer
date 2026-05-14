defmodule ClientType_ do
  def post(_data), do: nil
end
defmodule ApiType_ do
  def client, do: ClientType_
end
defmodule ObjType_ do
  def api, do: ApiType_
end
defmodule Check do
  def x do
    obj = ObjType_
    obj.api.client.post("hello")
    obj.api.client.post(42)
    obj.api.client.post(true)
  end
end
