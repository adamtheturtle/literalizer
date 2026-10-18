function f {}
$ref_data = @(
    ,@(
        1;
        2
    );
    ,@(
        3;
        4
    )
)
f @(
    ,@(
        $ref_data
    )
)
