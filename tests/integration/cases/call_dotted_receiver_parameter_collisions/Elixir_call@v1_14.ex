defmodule WorkerType_ do
  def process(_self, _self_), do: nil
end
defmodule Check do
  def x do
    api = %{worker: WorkerType_}
    api.worker.process(%{}, %{})
  end
end
