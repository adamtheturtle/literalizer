defmodule Check do
  def process(_data), do: nil
  def x do
    known_value = 1
    unknown_value = []
    process(unknown_value)
  end
end
