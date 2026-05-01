defmodule Check do
  def send(_value), do: nil
  def x do
    send(%{"a" => 1, "b" => "x"})
  end
end
