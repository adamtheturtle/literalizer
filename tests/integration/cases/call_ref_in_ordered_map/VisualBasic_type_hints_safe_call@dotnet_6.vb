Imports System.Collections.Generic
Module Check
    Function process(a As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim big_list = New String() {
            "x"
        }
        process(New Dictionary(Of String, Object) From {{"m", big_list}})
    End Sub
End Module
