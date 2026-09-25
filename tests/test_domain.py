from agent_domain import *
def test_task_budget():
 t=Task("1");t.start();t.finish(True);assert t.state==TaskState.SUCCEEDED
