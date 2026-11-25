with A_Stub; use A_Stub;
procedure Main is
    std : A_Val := AMap'[
        AEntry ("a", AInt (1))
    ];
    arena : A_Val := AMap'[
        AEntry ("a", AInt (1))
    ];
    allocator : A_Val := AMap'[
        AEntry ("a", AInt (1))
    ];
    my_data : A_Val := AList'[
        std,
        arena,
        allocator
    ];
begin
    null;
end Main;
