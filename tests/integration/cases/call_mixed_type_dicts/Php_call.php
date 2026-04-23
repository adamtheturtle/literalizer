<?php
class MType { function Op($operation) {} }
$m = new MType();
$m->Op(operation: ["type" => "create", "pr_id" => "pr_1", "draft" => true]);
$m->Op(operation: ["type" => "create", "pr_id" => "pr_2"]);
