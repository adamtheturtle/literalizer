Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' # section
        Dim my_data = New String() {
            "a"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' # section
        my_data = New String() {
            "a"
        }
    End Sub
End Module
