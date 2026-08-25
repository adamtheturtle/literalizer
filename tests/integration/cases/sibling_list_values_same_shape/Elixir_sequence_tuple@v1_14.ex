defmodule Check do
  def x do
    my_data = %{
        "test" => {5, {"compile", "test"}},
        "package" => {7, {"link", "test"}},
    }
    _ = my_data
  end
end
