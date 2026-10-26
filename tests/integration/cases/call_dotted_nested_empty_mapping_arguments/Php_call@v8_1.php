<?php
class WorkerType { function process($values, $count) {} }
class ApiType { public $worker; function __construct() { $this->worker = new WorkerType(); } }
$api = new ApiType();
$api->worker->process(values: [1, []], count: 42);
$api->worker->process(values: [2, ["x" => "s"]], count: 43);
