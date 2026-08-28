defmodule Check do
  def x do
    my_data = %{
        "first" => [
            1,
            2,
        ],
        "second" => 3,  # About the second key.
    }
    _ = my_data
  end
end
