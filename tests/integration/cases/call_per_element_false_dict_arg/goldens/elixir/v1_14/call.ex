defmodule Check do
  def process(_value), do: nil
  def x do
    process(%{"a" => 1, "b" => "x"})
  end
end
