Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String() {
            "foo",
            "bar",
            "baz"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String() {
            "foo",
            "bar",
            "baz"
        }
    End Sub
End Module
