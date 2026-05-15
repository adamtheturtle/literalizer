defmodule Check do
  def x do
    my_data = %{
        # before
        "answer" => 42,  # inline
        "plain" => "ok",
        # trailing
    }
    _ = my_data
  end
end
