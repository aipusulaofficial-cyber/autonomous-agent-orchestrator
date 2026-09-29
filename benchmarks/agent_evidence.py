import json
from agent_domain import Task,ToolPolicy
t=Task("evidence",max_attempts=2); t.start(); t.finish(False); t.retry(); t.start(); t.finish(True)
p=ToolPolicy(frozenset({"search"})); allowed=False; blocked=False; p.authorize("search"); allowed=True
try: p.authorize("shell")
except PermissionError: blocked=True
report={"final_state":t.state.value,"attempts":t.attempts,"tool_allowed":allowed,"tool_blocked":blocked}
if report!={"final_state":"succeeded","attempts":2,"tool_allowed":True,"tool_blocked":True}: raise SystemExit(report)
print(json.dumps(report, sort_keys=True))
