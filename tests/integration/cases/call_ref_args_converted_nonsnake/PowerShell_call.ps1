function process {}
$MyVar = @(
    1;
    2;
    3
)
$MyOther = @(
    4;
    5;
    6
)
process($MyVar, 42)
process($MyOther, 7)
