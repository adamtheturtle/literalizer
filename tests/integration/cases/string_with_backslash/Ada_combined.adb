procedure Check is
   procedure Check_Declaration is
      my_data : A_Val := AList'(
          AStr ("C:\path\to\file"),
          AStr ("back\\slash"),
          AStr ("hello \""world\"""),
          AStr ("path\to ""# file")
      );
   begin
      null;
   end Check_Declaration;
   procedure Check_Assignment is
   begin
      my_data := AList'(
          AStr ("C:\path\to\file"),
          AStr ("back\\slash"),
          AStr ("hello \""world\"""),
          AStr ("path\to ""# file")
      );
   end Check_Assignment;
begin
   Check_Declaration;
   Check_Assignment;
end Check;
