from typing import List

import numpy as np

from . import util
from .api import PhysicsModel, DataModel


class Omniscient(DataModel):
    """A data-driven model intended for testing.  Given a sequence of intended
    (and arbitrary) solutions, and access to the physics-based model, this DDM
    will provide 'perfect' corrections.

    This assumes that the DDM will be called to make predictions exactly once
    per timestep.
    """

    def __init__(self, pbm: PhysicsModel, solutions: List[np.ndarray]):
        self.pbm = pbm
        self.dirichlet_dofs = np.array(pbm.dirichlet_dofs(), dtype=int) - 1
        self.solutions = list(solutions)

    def __call__(self, params, upred: np.ndarray) -> np.ndarray:
        uprev = util.to_external(self.solutions.pop(0), dofs=self.dirichlet_dofs)
        unext = util.to_external(self.solutions[0], dofs=self.dirichlet_dofs)
        sigma = self.pbm.residual(params, uprev, unext)
        return -util.to_internal(sigma, dofs=self.dirichlet_dofs)