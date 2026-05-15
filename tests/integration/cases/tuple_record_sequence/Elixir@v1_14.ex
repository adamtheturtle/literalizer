defmodule Check do
  def x do
    my_data = [
        %{"call" => "send", "args" => [1, "email", "a@gmail.com", 100]},
        %{"call" => "recv", "args" => [2, "sms", "b@example.com", 200]},
    ]
    _ = my_data
  end
end
