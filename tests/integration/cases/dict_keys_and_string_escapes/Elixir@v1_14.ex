defmodule Check do
  def x do
    my_data = %{
        "plain" => [1, 2],
        "with-dash" => "a\nb",
    }
    _ = my_data
  end
end
