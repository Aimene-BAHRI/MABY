PyKnow: Expert Systems for Python
=================================

.. image:: https://img.shields.io/pypi/v/pyknow.svg
    :target: https://pypi.python.org/pypi/pyknow

.. image:: https://img.shields.io/pypi/pyversions/pyknow.svg
    :target: https://pypi.python.org/pypi/pyknow

.. image:: https://travis-ci.org/buguroo/pyknow.svg?branch=master
    :target: https://travis-ci.org/buguroo/pyknow

.. image:: https://readthedocs.org/projects/pyknow/badge/?version=latest
    :target: https://readthedocs.org/projects/pyknow/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/buguroo/pyknow/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/buguroo/pyknow
    :alt: codecov.io


PyKnow is a Python library for building expert systems strongly inspired
by CLIPS_.

.. code-block:: python

   from random import choice
   from pyknow import *


   class Light(Fact):
       """Info about the traffic light."""
       pass


   class RobotCrossStreet(KnowledgeEngine):
       @Rule(Light(color='green'))
       def green_light(self):
           print("Walk")

       @Rule(Light(color='red'))
       def red_light(self):
           print("Don't walk")

       @Rule('light' << Light(color=L('yellow') | L('blinking-yellow')))
       def cautious(self, light):
           print("Be cautious because light is", light["color"])


.. code-block:: python

   >>> engine = RobotCrossStreet()
   >>> engine.reset()
   >>> engine.declare(Light(color=choice(['green', 'yellow', 'blinking-yellow', 'red'])))
   >>> engine.run()
   Be cautious because light is blinking-yellow


You can find some more examples on GitHub_.

.. _CLIPS: http://clipsrules.sourceforge.net
.. _GitHub: https://github.com/buguroo/pyknow/tree/develop/docs/examples

