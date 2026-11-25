Imports System.Collections.Generic
Module Check
    Function process(a As Object, b As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim big_list = New String() {
            "x"
        }
        process(New Dictionary(Of String, Object) From {{"k", big_list}}, 2)
    End Sub
End Module
