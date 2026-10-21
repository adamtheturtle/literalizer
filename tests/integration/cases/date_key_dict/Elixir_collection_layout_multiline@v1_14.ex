defmodule Check do
  def x do
    my_data = %{
        ~D[2024-01-01] => "new_year",
        ~D[2024-07-04] => "independence_day",
        ~D[2024-12-25] => "christmas",
    }
    _ = my_data
  end
end
