defmodule Check do
  def process(_known_value, _nested_missing), do: nil
  def x do
    known_value = true
    unknown_value = true
    process(known_value, [unknown_value])
  end
end
