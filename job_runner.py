from dataclasses import dataclass,field
from enum import Enum
class State(str,Enum): PLANNED="planned"; RUNNING="running"; SUCCEEDED="succeeded"; FAILED="failed"
@dataclass
class Job: id:str; actions:list[str]; state:State=State.PLANNED; audit:list[str]=field(default_factory=list)
class JobRunner:
 def __init__(self,allowed,max_actions=8): self.allowed=allowed; self.max_actions=max_actions
 def run(self,j):
  if len(j.actions)>self.max_actions: raise ValueError("action budget exceeded")
  j.state=State.RUNNING;j.audit.append("started")
  try:
   for name in j.actions:
    if name not in self.allowed: raise KeyError(name)
    self.allowed[name]();j.audit.append("action:"+name)
   j.state=State.SUCCEEDED;j.audit.append("completed");return j
  except Exception as e:
   j.state=State.FAILED;j.audit.append("failed:"+type(e).__name__);raise
