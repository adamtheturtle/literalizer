defmodule Check do
  def x do
    my_data = %{
        "a-b" => 1,
        "two words" => 2,
        "she said \"hi\"" => 3,
        "" => 4,
        "valid_key" => 5,
    }
    _ = my_data
  end
end
