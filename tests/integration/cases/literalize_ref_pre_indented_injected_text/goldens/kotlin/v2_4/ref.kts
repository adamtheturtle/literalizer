            val shared = intArrayOf(
                1,
                2,
            )
            val other = 3
            val payload = "\n    shared : Val\nshared = RInt 99"
            val my_data = mapOf<String, Any?>(
                "a" to shared,
                "b" to other,
                "payload" to payload,
            )
