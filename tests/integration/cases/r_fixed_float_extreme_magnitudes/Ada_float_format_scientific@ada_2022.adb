with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AFloat (5.0e-324),
        AFloat (2.2250738585072014e-308),
        AFloat (1.0e-307),
        AFloat (1.0e21),
        AFloat (-1.5e300),
        AFloat (1.7976931348623157e308),
        AFloat (-1.7976931348623157e308)
    ];
begin
    null;
end Main;
