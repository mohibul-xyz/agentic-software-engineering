## example schema
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


## tool call result
{
  "type": "tool_call",
  "id": "call_1",
  "name": "lookup_notice",
  "arguments": {
    "notice_id": "N-042"
  }
}

{
  "type": "tool_result",
  "tool_call_id": "call_1",
  "ok": true,
  "data": {
    "notice_id": "N-042",
    "text": "Applications close on 30 November 2026."
  }
}


## Observation
{
  "type": "tool_result",
  "tool_call_id": "call_1",
  "ok": false,
  "error": {
    "code": "TEMPORARY_TIMEOUT",
    "message": "The notice service did not respond in time.",
    "retryable": true
  }
}


## One run record per task attempt
{
  "task_id": "notice-042-deadline",
  "run_id": "run-002",
  "status": "completed",
  "model_steps": 3,
  "tool_calls_requested": 2,
  "tool_calls_executed": 2,
  "usage": {
    "input_tokens": 1200,
    "output_tokens": 180
  },
  "cost_usd": 0.0018,
  "wall_clock_ms": 2140,
  "steps": [
    {"step": 1, "decision": "tool_call", "call_id": "call_1", "outcome": "TEMPORARY_TIMEOUT"},
    {"step": 2, "decision": "tool_call", "call_id": "call_2", "outcome": "ok"},
    {"step": 3, "decision": "final", "outcome": "valid_json"}
  ]
}
