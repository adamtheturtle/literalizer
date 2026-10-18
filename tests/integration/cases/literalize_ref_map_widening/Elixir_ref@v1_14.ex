defmodule Check do
  def x do
    string_map = %{
        "k" => "s",
    }
    my_data = [
        string_map,
        %{"k" => 1},
    ]
    _ = my_data
  end
end
