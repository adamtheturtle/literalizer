<?php
class ThrottlerType { function check() {} }
$throttler = new ThrottlerType();
$throttler->check();
$throttler->check();
