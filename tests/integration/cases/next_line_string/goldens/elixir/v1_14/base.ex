defmodule Check do
  def x do
    my_data = %{
        "x" => "\u0085",
    }
    _ = my_data
  end
end
