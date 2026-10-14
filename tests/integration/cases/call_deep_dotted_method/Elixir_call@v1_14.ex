defmodule ClientType_ do
  def post(_data), do: nil
end
defmodule Check do
  def x do
    obj = %{api: %{client: ClientType_}}
    obj.api.client.post("hello")
    obj.api.client.post(42)
    obj.api.client.post(true)
  end
end
