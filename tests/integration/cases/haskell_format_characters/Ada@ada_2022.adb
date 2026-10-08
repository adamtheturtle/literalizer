with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("v", AStr ("a­​‍‎‮⁠﻿" & Character'Val(226) & Character'Val(128) & Character'Val(168) & Character'Val(226) & Character'Val(128) & Character'Val(169) & "b")),
        AEntry ("a­​‍‎‮⁠﻿" & Character'Val(226) & Character'Val(128) & Character'Val(168) & Character'Val(226) & Character'Val(128) & Character'Val(169) & "b", AInt (1))
    ];
begin
    null;
end Main;
