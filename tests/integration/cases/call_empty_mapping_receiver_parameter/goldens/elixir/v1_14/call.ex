defmodule ApiType_ do
  def process(_self), do: nil
end
defmodule Check do
  def x do
    api = ApiType_
    api.process(%{})
  end
end
