defmodule Check do
  def consume(_value), do: nil
  def x do
    item = nil
    consume(item)
  end
end
