with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("lower", AInt (3735928559)),
        AEntry ("upper", AInt (31)),
        AEntry ("negative", AInt (-16)),
        AEntry ("zero", AInt (0))
    ];
begin
    null;
end Main;
