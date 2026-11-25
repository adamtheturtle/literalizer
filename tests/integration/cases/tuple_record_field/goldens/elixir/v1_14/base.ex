defmodule Check do
  def x do
    my_data = %{
        "call" => "send",
        "args" => [1, "email", "a@gmail.com", 100],
    }
    _ = my_data
  end
end
