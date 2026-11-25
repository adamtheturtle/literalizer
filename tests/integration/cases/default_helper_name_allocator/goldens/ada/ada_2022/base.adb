with A_Stub; use A_Stub;
procedure Main is
    allocator : A_Val := AMap'[
        AEntry ("a", AInt (1))
    ];
begin
    null;
end Main;
