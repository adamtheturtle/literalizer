defmodule Check do
  def process(_data), do: nil
  def x do
    untyped_value = {}
    process({untyped_value, untyped_value})
  end
end
