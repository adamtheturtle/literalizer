defmodule Check do
  def x do
    my_data = %{
        "ancient_date" => ~D[1500-03-01],
        "modern_date" => ~D[2024-01-15],
        "before_date" => ~D[1582-10-04],
        "gap_date" => ~D[1582-10-10],
        "transition_date" => ~D[1582-10-15],
        "after_date" => ~D[1582-10-16],
        "before_naive" => ~N[1582-10-04 12:30:00.000001],
        "gap_naive" => ~N[1582-10-10 12:30:00.500000],
        "transition_positive" => ~U[1582-10-14 06:30:00+00:00],
        "transition_negative" => ~U[1582-10-16 17:30:00+00:00],
        "after_positive" => ~U[1582-10-15 06:30:00+00:00],
    }
    _ = my_data
  end
end
