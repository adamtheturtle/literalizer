defmodule Check do
  def put(_key, _value), do: nil
  def get(_key), do: nil
  def x do
    put(1, 10)
    get(1)
  end
end
