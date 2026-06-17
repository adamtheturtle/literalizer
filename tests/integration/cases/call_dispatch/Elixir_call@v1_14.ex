defmodule Check do
  def store_item(_key, _value), do: nil
  def read_item(_key), do: nil
  def x do
    store_item(1, 10)
    read_item(1)
  end
end
