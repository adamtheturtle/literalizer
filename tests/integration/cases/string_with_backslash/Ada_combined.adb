procedure Check is
   procedure Check_Declaration is
      my_data : A_Val := AList'(
          AStr ("C:\path\to\file"),
          AStr ("back\\slash"),
          AStr ("hello \""world\"""),
          AStr ("path\to ""# file"),
          AStr ("trailing\"),
          AStr ("both ""quotes''' here")
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
          AStr ("path\to ""# file"),
          AStr ("trailing\"),
          AStr ("both ""quotes''' here")
      );
   end Check_Assignment;
begin
   Check_Declaration;
   Check_Assignment;
end Check;
