defmodule Check do
  def x do
    my_data = [
        %{"type" => "create", "name" => "a"},
        %{"type" => "update", "name" => "b"},
    ]
    _ = my_data
  end
end
