defmodule Check do
  def consume(_value), do: nil
  def x do
    external_value = 1
    consume(external_value)
  end
end
