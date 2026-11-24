Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String() {
            "中中中中中中中中中中中中中中中中中中中中",
            "é'é'é'é'é'é'é'é'é'é'",
            "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String() {
            "中中中中中中中中中中中中中中中中中中中中",
            "é'é'é'é'é'é'é'é'é'é'",
            "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
        }
    End Sub
End Module
