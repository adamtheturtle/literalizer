Imports System.Collections.Generic
Module Check
    Function process(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        process("Dune")  ' first edition
        process("Solaris")
        process("Neuromancer")  ' cyberpunk
    End Sub
End Module
