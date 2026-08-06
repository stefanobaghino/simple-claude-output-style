"""The campaign driver.

A campaign is several full pair runs under identical conditions. The
driver runs the documented schedule: serialized pair stages,
overlapped judge stages, the value pass split around the loss pass,
and one worker budget across every stage.
"""

from .schedule import Scheduler, StageResult, StageSpec

__all__ = ["Scheduler", "StageResult", "StageSpec"]
