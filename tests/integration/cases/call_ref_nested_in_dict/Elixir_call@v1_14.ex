defmodule Check do
  def process(_data), do: nil
  def x do
    my_var = 42
    process(%{"key" => my_var, "count" => 42, "label" => "example"})
  end
end
