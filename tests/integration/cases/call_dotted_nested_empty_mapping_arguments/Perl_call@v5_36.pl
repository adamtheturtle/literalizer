sub api {}
sub worker {}
sub process {}
api.worker.process([1, {}], 42);
api.worker.process([2, {"x" => "s"}], 43);
