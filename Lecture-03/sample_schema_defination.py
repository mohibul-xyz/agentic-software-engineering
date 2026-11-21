assignment_status_tool = {
    "name": "get_assignment_status",
    "description": "Look up a student's submission status for one assignment.",
    "parameters": {
        "type": "object",
        "properties": {
            "student_id": {
                "type": "string",
                "description": "The student's ID, such as 'S-101'.",
                "minLength": 1,
            },
            "assignment_number": {
                "type": "integer",
                "description": "The assignment number in the course.",
                "minimum": 1,
            },
        },
        "required": ["student_id", "assignment_number"],
        "additionalProperties": False,
    },
}

assignment_status_output_schema = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["submitted", "no_record"],
        },
    },
    "required": ["status"],
    "additionalProperties": False,
}
