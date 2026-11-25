defmodule Check do
  def x do
    my_data = %{
        "outer" => [["nested first line\n  indented\n\nnested last line\n"]],
    }
    _ = my_data
  end
end
