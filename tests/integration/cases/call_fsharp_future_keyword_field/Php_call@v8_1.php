<?php
class ProcessType { function fetch($data) {} }
class AppType { public $process; function __construct() { $this->process = new ProcessType(); } }
$app = new AppType();
$app->process->fetch(data: ["data" => "hello"]);
$app->process->fetch(data: ["data" => 42]);
$app->process->fetch(data: ["data" => true]);
