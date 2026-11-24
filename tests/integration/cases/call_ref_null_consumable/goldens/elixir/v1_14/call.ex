defmodule Check do
  def consume(_value), do: nil
  def x do
    my_null = nil
    regular_null = nil
    consume(my_null)
    consume(regular_null)
  end
end
