defmodule Check do
  def x do
    my_data = %{
        "name" => "Alice",
        "tags" => MapSet.new([
            true,
            42,
            "apple",
        ]),
    }
    _ = my_data
  end
end
