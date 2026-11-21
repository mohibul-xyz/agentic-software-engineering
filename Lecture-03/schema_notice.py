{
  "name": "lookup_notice",
  "description": "Fetch a notice by its ID and return its text.",
  "parameters": {
    "type": "object",
    "properties": {
      "notice_id": {
        "type": "string",
        "pattern": "^N-[0-9]{3}$"
      }
    },
    "required": ["notice_id"],
    "additionalProperties": false
  }
}
