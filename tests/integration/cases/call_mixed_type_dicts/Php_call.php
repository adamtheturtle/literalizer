<?php
class MgrType { function run($operation) {} }
class AppType { public $mgr; function __construct() { $this->mgr = new MgrType(); } }
$app = new AppType();
$app->mgr->run(operation: ["type" => "create", "pr_id" => "pr_1", "draft" => true]);
$app->mgr->run(operation: ["type" => "create", "pr_id" => "pr_2"]);
