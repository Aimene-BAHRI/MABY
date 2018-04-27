from collections import deque
import abc
import logging

from pyknow import watchers


class Matcher(metaclass=abc.ABCMeta):
    def __init__(self, engine):
        self.engine = engine

    @abc.abstractmethod
    def changes(self, adding=None, deleting=None):  # pragma: no cover
        """
        Main interface with the matcher.

        Called by the knowledge engine when changes are made in the
        working memory and return a set of activations.

        """
        pass

    @abc.abstractmethod
    def reset(self):  # pragma: no cover
        """Reset the matcher memory."""
        pass


class Strategy(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resolved = dict()

    @abc.abstractmethod
    def _update_agenda(self, agenda, added, removed):  # pragma: no cover
        pass

    def update_agenda(self, agenda, added, removed):
        if watchers.ACTIVATIONS.level <= logging.INFO:
            for act in removed:
                watchers.ACTIVATIONS.info(
                    " <== %r: %s %s",
                    getattr(act.rule, '__name__', None),
                    ", ".join(str(f) for f in act.facts),
                    "[EXECUTED]" if act not in agenda.activations else "")

            for act in added:
                watchers.ACTIVATIONS.info(
                    " ==> %r: %s",
                    getattr(act.rule, '__name__', None),
                    ", ".join(str(f) for f in act.facts))

        # Resolve conflicts using the appropiate strategy.
        new_activations = deque(self._update_agenda(agenda, added, removed))
        if new_activations != agenda.activations:
            agenda.activations = new_activations
