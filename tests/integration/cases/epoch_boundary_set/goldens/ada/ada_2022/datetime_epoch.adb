with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := ASet'[
        AInt (-2147483649),
        AInt (-2147483648),
        AInt (2147483647),
        AInt (2147483648)
    ];
begin
    null;
end Main;
