def grade_deadline(answer, expected_deadline):
    if not isinstance(answer, dict):
        return False

    return answer.get("deadline") == expected_deadline


grade_deadline({"deadline": "2026-11-30"}, "2026-11-30")  # True
grade_deadline({"deadline": "2026-11-15"}, "2026-11-30")  # False
