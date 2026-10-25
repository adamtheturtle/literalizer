defmodule WorkerType_ do
  def process(_values, _count), do: nil
end
defmodule Check do
  def x do
    api = %{worker: WorkerType_}
    api.worker.process([1, %{}], 42)
    api.worker.process([2, %{"x" => "s"}], 43)
  end
end
