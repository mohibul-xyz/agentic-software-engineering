import unittest
from copy import deepcopy


def run_agent(question, model, lookup_notice, max_steps=3):
    messages = [{"role": "user", "content": question}]

    for _ in range(max_steps):
        reply = model(messages)

        if not isinstance(reply, dict):
            return {"status": "malformed_reply"}

        if reply.get("type") == "final" and isinstance(reply.get("answer"), str):
            return {"status": "completed", "answer": reply["answer"]}

        if (
            reply.get("type") != "tool_call"
            or reply.get("name") != "lookup_notice"
            or not isinstance(reply.get("notice_id"), str)
        ):
            return {"status": "malformed_reply"}

        messages.append({"role": "assistant", "content": reply})

        try:
            notice_text = lookup_notice(reply["notice_id"])
            observation = {"ok": True, "text": notice_text}
        except TimeoutError:
            observation = {"ok": False, "error": "timeout"}

        messages.append({"role": "tool", "content": observation})

    return {"status": "step_limit"}


class ScriptedLM:
    def __init__(self, replies):
        self.replies = iter(replies)
        self.requests = []

    def __call__(self, messages):
        # Save the conversation as it looked at the time of this call.
        self.requests.append(deepcopy(messages))

        try:
            return next(self.replies)
        except StopIteration:
            raise AssertionError("The agent made an unexpected model call") from None


QUESTION = "What is the deadline for notice N-042?"
NOTICE = "Applications close on 30 November 2026."
LOOKUP = {
    "type": "tool_call",
    "name": "lookup_notice",
    "notice_id": "N-042",
}
FINAL = {"type": "final", "answer": "2026-11-30"}


class TestAgentLoop(unittest.TestCase):
    def test_successful_lookup_result_reaches_model(self):
        model = ScriptedLM([LOOKUP, FINAL])
        looked_up_ids = []

        def lookup_notice(notice_id):
            looked_up_ids.append(notice_id)
            return NOTICE

        result = run_agent(QUESTION, model, lookup_notice)

        self.assertEqual(result, {"status": "completed", "answer": "2026-11-30"})
        self.assertEqual(looked_up_ids, ["N-042"])
        self.assertEqual(len(model.requests), 2)
        self.assertIn(
            {"role": "tool", "content": {"ok": True, "text": NOTICE}},
            model.requests[1],
        )

    def test_malformed_reply_stops_without_running_tool(self):
        # This tool request is missing notice_id.
        model = ScriptedLM([{"type": "tool_call", "name": "lookup_notice"}])

        def lookup_notice(notice_id):
            self.fail("The loop ran a tool with malformed arguments")

        result = run_agent(QUESTION, model, lookup_notice)

        self.assertEqual(result, {"status": "malformed_reply"})
        self.assertEqual(len(model.requests), 1)

    def test_tool_timeout_reaches_model_and_retry_can_succeed(self):
        model = ScriptedLM([LOOKUP, LOOKUP, FINAL])
        looked_up_ids = []

        def lookup_notice(notice_id):
            looked_up_ids.append(notice_id)
            if len(looked_up_ids) == 1:
                raise TimeoutError("The notice service took too long")
            return NOTICE

        result = run_agent(QUESTION, model, lookup_notice)

        self.assertEqual(result, {"status": "completed", "answer": "2026-11-30"})
        self.assertEqual(looked_up_ids, ["N-042", "N-042"])
        self.assertEqual(len(model.requests), 3)
        self.assertEqual(
            model.requests[1][-1],
            {"role": "tool", "content": {"ok": False, "error": "timeout"}},
        )
        self.assertEqual(
            model.requests[2][-1],
            {"role": "tool", "content": {"ok": True, "text": NOTICE}},
        )

    def test_step_cap_prevents_a_third_model_call(self):
        model = ScriptedLM([LOOKUP, LOOKUP, FINAL])

        def lookup_notice(notice_id):
            return NOTICE

        result = run_agent(QUESTION, model, lookup_notice, max_steps=2)

        self.assertEqual(result, {"status": "step_limit"})
        self.assertEqual(len(model.requests), 2)


if __name__ == "__main__":
    unittest.main()
