Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String() {
            "prefix ${HOME} suffix",
            "${interpolated}"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String() {
            "prefix ${HOME} suffix",
            "${interpolated}"
        }
    End Sub
End Module
