from dataclasses import dataclass

import numpy as np


@dataclass
class Player:
    name: str
    id: np.int64
    tier: str
    rank: str
    level: np.int64