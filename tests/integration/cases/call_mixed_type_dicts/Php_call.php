<?php
class MgrType { function Op($operation) {} }
$mgr = new MgrType();
$mgr->Op(operation: ["type" => "create", "pr_id" => "pr_1", "draft" => true]);
$mgr->Op(operation: ["type" => "create", "pr_id" => "pr_2"]);
