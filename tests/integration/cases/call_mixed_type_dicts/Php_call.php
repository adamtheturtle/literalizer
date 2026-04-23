<?php
class MgrType { function op($operation) {} }
class AppType { public $mgr; function __construct() { $this->mgr = new MgrType(); } }
$app = new AppType();
$app->mgr->op(operation: ["type" => "create", "pr_id" => "pr_1", "draft" => true]);
$app->mgr->op(operation: ["type" => "create", "pr_id" => "pr_2"]);
