defmodule Check do
  def process(_data), do: nil
  def x do
    my_var = 42
    process([%{"ref" => "myVar"}, 42, "static"])
  end
end
