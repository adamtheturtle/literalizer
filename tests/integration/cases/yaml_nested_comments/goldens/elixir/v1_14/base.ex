defmodule Check do
  def x do
    my_data = %{
        "a" => %{
            # inner note
            "b" => 1,  # inline b
        },
        "list" => [
            1,  # first
            2,  # second
        ],
    }
    _ = my_data
  end
end
