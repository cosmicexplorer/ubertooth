# coding=utf-8

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import os

from pants_test.pants_run_integration_test import PantsRunIntegrationTest


class TestOsLibIntegration(PantsRunIntegrationTest):

  def test_transmit_audio_pydist(self):
    pants_run = self.run_pants(['-q', 'run-hack', 'aptx-transmission:bin'])
    self.assert_success(pants_run)
    self.assertEqual('5\n', pants_run.stdout_data)
