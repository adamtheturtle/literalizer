defmodule Check do
  def process(_data), do: nil
  def x do
    unknown_value = [
        1,
    ]
    process(unknown_value)
  end
end
