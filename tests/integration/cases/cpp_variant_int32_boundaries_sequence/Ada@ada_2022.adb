with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AInt (-2147483648),
        AInt (-2147483647),
        AList'[AInt (0)]
    ];
begin
    null;
end Main;
