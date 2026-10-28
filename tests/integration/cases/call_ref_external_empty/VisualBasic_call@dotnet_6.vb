Imports System.Collections.Generic
Module Check
    Function consume(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim item = New Integer() {
            1,
            2
        }
        consume(item)
    End Sub
End Module
