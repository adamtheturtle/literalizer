defmodule Check do
  def consume(_value), do: nil
  def x do
    consume(-2147483649)
    consume(2147483648)
  end
end
