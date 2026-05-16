defmodule Check do
  def x do
    my_data = [
        %{"id" => 1, "empty_map" => %{}, "int_map" => %{1 => "a"}, "full_set" => MapSet.new(["x", "y"]), "empty_set" => MapSet.new()},
        %{"id" => 2, "empty_map" => %{}, "int_map" => %{1 => "b"}, "full_set" => MapSet.new(["x"]), "empty_set" => MapSet.new()},
    ]
    _ = my_data
  end
end
