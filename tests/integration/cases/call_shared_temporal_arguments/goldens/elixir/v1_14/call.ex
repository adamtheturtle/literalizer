defmodule Check do
  def check(_timestamp, _date_value), do: nil
  def x do
    check("2024-01-15T10:30:00+00:00", ~D[2024-06-01])
  end
end
