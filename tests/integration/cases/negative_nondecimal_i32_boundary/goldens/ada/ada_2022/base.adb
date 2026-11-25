with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("minimum", AInt (-2147483648)),
        AEntry ("below", AInt (-3000000000))
    ];
begin
    null;
end Main;
