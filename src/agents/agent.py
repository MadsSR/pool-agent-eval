import fastfiz as ff
from typing import Optional


class Agent:
    def decide_shot(self, table_state: ff.TableState) -> Optional[ff.ShotParams]:
        raise NotImplementedError
