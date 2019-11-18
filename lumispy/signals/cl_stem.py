#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019 The LumiSpy developers
#
# This file is part of lumispy.
#
# lumispy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lumispy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lumispy.  If not, see <http://www.gnu.org/licenses/>.

"""Signal class for cathodoluminescence spectral data acquired in STEM.

"""

import numpy as np

from lumispy.signals.cl import CLSpectrum
from hyperspy._signals.lazy import LazySignal


class CLSTEMSpectrum(CLSpectrum):
    _signal_type = "cl_spectrum"

    def __init__(self, *args, **kwargs):
        self, args, kwargs = push_metadata_through(self, *args, **kwargs)
        super().__init__(*args, **kwargs)

    def as_lazy(self, *args, **kwargs):
        """Create a copy of the CLSTEMSpectrum object as a
        :py:class:`~lumispy.signals.cl.CLSTEMSpectrum`.

        Parameters
        ----------
        copy_variance : bool
            If True variance from the original CLSTEMSpectrum object is copied to
            the new CLSTEMSpectrum object.

        Returns
        -------
        res : :py:class:`~lumispy.signals.cl.LazyCLSTEMSpectrum`.
            The lazy signal.
        """
        res = super().as_lazy(*args, **kwargs)
        res.__class__ = LazyCLSTEMSpectrum
        res.__init__(**res._to_dictionary())
        return res

    def decomposition(self, *args, **kwargs):
        super().decomposition(*args, **kwargs)
        self.__class__ = CLSTEMSpectrum


class LazyCLSTEMSpectrum(LazySignal, CLSTEMSpectrum):

    _lazy = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute(self, *args, **kwargs):
        super().compute(*args, **kwargs)
        self.__class__ = CLSTEMSpectrum
        self.__init__(**self._to_dictionary())

    def decomposition(self, *args, **kwargs):
        super().decomposition(*args, **kwargs)
        self.__class__ = LazyCLSTEMSpectrum