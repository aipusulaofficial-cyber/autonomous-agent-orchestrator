from dataclasses import dataclass
from enum import StrEnum

class TaskState(StrEnum): PENDING="pending"; RUNNING="running"; SUCCEEDED="succeeded"; FAILED="failed"; CANCELLED="cancelled"

@dataclass
class Task:
    id:str; state:TaskState=TaskState.PENDING; attempts:int=0
    def start(self):
        if self.state is not TaskState.PENDING: raise ValueError("task not pending")
        self.state=TaskState.RUNNING; self.attempts+=1
    def finish(self,ok:bool):
        if self.state is not TaskState.RUNNING: raise ValueError("task not running")
        self.state=TaskState.SUCCEEDED if ok else TaskState.FAILED

def enforce_step_budget(completed:int,limit:int)->None:
    if completed>=limit: raise RuntimeError("agent step budget exhausted")
