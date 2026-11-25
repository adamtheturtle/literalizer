defmodule Check do
  def process(_value), do: nil
  def x do
    process(%{"value" => 1})
    process(%{"value" => "hello"})
  end
end
