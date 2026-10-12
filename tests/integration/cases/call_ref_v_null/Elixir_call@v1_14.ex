defmodule Check do
  def consume(_value), do: nil
  def x do
    value = nil
    consume(value)
  end
end
