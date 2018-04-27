"""
``pyknow engine`` represents ``CLIPS modules``

"""

from inspect import getmembers
import logging
import warnings

from pyknow import abstract

from pyknow.agenda import Agenda
from pyknow.fact import InitialFact
from pyknow.factlist import FactList
from pyknow.rule import Rule
from pyknow.deffacts import DefFacts
from pyknow import watchers

logging.basicConfig()


class KnowledgeEngine:
    """
    This represents a clips' ``module``, wich is an ``inference engine``
    holding a set of ``rules`` (as :obj:`pyknowlib.rule.Rule` objects),
    an ``agenda`` (as :obj:`pyknowlib.agenda.Agenda` object)
    and a ``fact-list`` (as :obj:`pyknowlib.factlist.FactList` objects)

    This could be considered, when inherited from, as the
    ``knowlege-base``.
    """
    from pyknow.matchers import ReteMatcher as __matcher__
    from pyknow.strategies import DepthStrategy as __strategy__

    def __init__(self):
        self.running = False
        self.facts = FactList()
        self.agenda = Agenda()

        if (isinstance(self.__matcher__, type)
                and issubclass(self.__matcher__, abstract.Matcher)):
            self.matcher = self.__matcher__(self)
        else:
            raise TypeError("__matcher__ must be a subclass of Matcher")

        if (isinstance(self.__strategy__, type)
                and issubclass(self.__strategy__, abstract.Strategy)):
            self.strategy = self.__strategy__()
        else:
            raise TypeError("__strategy__ must be a subclass of Strategy")

    @staticmethod
    def _get_real_modifiers(**modifiers):
        for k, v in modifiers.items():
            if k.startswith('_') and k[1:].isnumeric():
                yield (int(k[1:]), v)
            else:
                yield (k, v)

    def modify(self, declared_fact, **modifiers):
        """

        Modifies a fact.

        Facts are inmutable in Clips, thus, as documented in clips
        reference manual, this retracts a fact and then re-declares it

        `modifiers` must be a Mapping object containing keys and values
        to be changed.

        To allow modifying positional facts, the user can pass a string
        containing the symbol "_" followed by the numeric index
        (starting with 0). Ex::

            >>> ke.modify(my_fact, _0="hello", _1="world", other_key="!")

        """
        self.retract(declared_fact)

        newfact = declared_fact.copy()
        newfact.update(dict(self._get_real_modifiers(**modifiers)))

        return self.declare(newfact)

    def duplicate(self, template_fact, **modifiers):
        """Create a new fact from an existing one."""

        newfact = template_fact.copy()
        newfact.update(dict(self._get_real_modifiers(**modifiers)))

        return self.declare(newfact)

    @DefFacts(order=-1)
    def _declare_initial_fact(self):
        yield InitialFact()

    def _get_by_type(self, wanted_type):
        for _, obj in getmembers(self):
            if isinstance(obj, wanted_type):
                obj.ke = self
                yield obj

    def get_rules(self):
        """Return the existing rules."""
        return list(self._get_by_type(Rule))

    def get_deffacts(self):
        """Return the existing deffacts sorted by the internal order"""
        return sorted(self._get_by_type(DefFacts), key=lambda d: d.order)

    def get_activations(self):
        """
        Return activations
        """
        return self.matcher.changes(*self.facts.changes)

    def retract(self, idx_or_declared_fact):
        """
        Retracts a specific fact, using its index

        .. note::
            This updates the agenda
        """
        self.facts.retract(idx_or_declared_fact)

        if not self.running:
            added, removed = self.get_activations()
            self.strategy.update_agenda(self.agenda, added, removed)

    def run(self, steps=float('inf')):
        """
        Execute agenda activations
        """

        self.running = True
        activation = None
        execution = 0
        while steps > 0 and self.running:

            added, removed = self.get_activations()
            self.strategy.update_agenda(self.agenda, added, removed)

            for idx, act in enumerate(self.agenda.activations):
                watchers.AGENDA.debug(
                    "%d: %r %r",
                    idx,
                    act.rule.__name__,
                    ", ".join(str(f) for f in act.facts))

            activation = self.agenda.get_next()

            if activation is None:
                break
            else:
                steps -= 1
                execution += 1

                watchers.RULES.info(
                    "FIRE %s %s: %s",
                    execution,
                    activation.rule.__name__,
                    ", ".join(str(f) for f in activation.facts))

                activation.rule(
                    self,
                    **{k: v
                       for k, v in activation.context.items()
                       if not k.startswith('__')})

        self.running = False

    def halt(self):
        self.running = False

    def reset(self):
        """
        Performs a reset as per CLIPS behaviour (resets the
        agenda and factlist and declares InitialFact())

        .. note:: If persistent facts have been added, they'll be
                  re-declared.
        """

        self.agenda = Agenda()
        self.facts = FactList()

        self.matcher.reset()

        # Declare all deffacts
        for deffact in self.get_deffacts():
            for fact in deffact():
                self.__declare(fact)

        self.running = False

    def __declare(self, *facts):
        """
        Internal declaration method. Used for ``declare`` and ``deffacts``
        """
        if any(f.has_field_constraints() for f in facts):
            raise TypeError(
                "Declared facts cannot contain conditional elements")
        else:
            last_inserted = None
            for fact in facts:
                last_inserted = self.facts.declare(fact)

            if not self.running:
                added, removed = self.get_activations()
                self.strategy.update_agenda(self.agenda, added, removed)

            return last_inserted

    def declare(self, *facts):
        """
        Declare from inside a fact, equivalent to ``assert`` in clips.

        .. note::

            This updates the agenda.
        """

        if not self.facts:
            warnings.warn("Declaring fact before reset()")
        return self.__declare(*facts)
