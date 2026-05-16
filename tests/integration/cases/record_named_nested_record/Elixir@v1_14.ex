defmodule Check do
  def x do
    my_data = %{
        "project" => "alpha",
        "lead_task" => %{"id" => 100, "description" => "first task", "is_done" => false, "blocks" => [102, 103]},
    }
    _ = my_data
  end
end
