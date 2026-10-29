<?php
class ApiType { function fetch($data) {} }
class ProcessType { public $api; function __construct() { $this->api = new ApiType(); } }
$process = new ProcessType();
$process->api->fetch(data: ["data" => "hello"]);
$process->api->fetch(data: ["data" => 42]);
$process->api->fetch(data: ["data" => true]);
