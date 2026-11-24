defmodule Check do
  def consume(_value), do: nil
  def x do
    consume(~N[1901-12-13 20:45:51])
    consume(~N[2038-01-19 03:14:08])
  end
end
