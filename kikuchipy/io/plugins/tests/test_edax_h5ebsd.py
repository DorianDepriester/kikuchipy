# Copyright 2019-2022 The kikuchipy developers
#
# This file is part of kikuchipy.
#
# kikuchipy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kikuchipy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kikuchipy. If not, see <http://www.gnu.org/licenses/>.

import os

from h5py import File
import pytest

from kikuchipy import load
from kikuchipy.conftest import assert_dictionary


DIR_PATH = os.path.dirname(__file__)
DATA_PATH = os.path.join(DIR_PATH, "../../../data")
EDAX_FILE = os.path.join(DATA_PATH, "edax_h5ebsd/patterns.h5")
AXES_MANAGER = {
    "axis-0": {
        "name": "y",
        "scale": 1.5,
        "offset": 0.0,
        "size": 3,
        "units": "um",
        "navigate": True,
    },
    "axis-1": {
        "name": "x",
        "scale": 1.5,
        "offset": 0.0,
        "size": 3,
        "units": "um",
        "navigate": True,
    },
    "axis-2": {
        "name": "dy",
        "scale": 1.0,
        "offset": 0.0,
        "size": 60,
        "units": "um",
        "navigate": False,
    },
    "axis-3": {
        "name": "dx",
        "scale": 1.0,
        "offset": 0.0,
        "size": 60,
        "units": "um",
        "navigate": False,
    },
}


class TestEDAXH5EBSD:
    def test_load(self):
        with File(EDAX_FILE, mode="r+") as f:
            grid = f["Scan 1/EBSD/Header/Grid Type"]
            grid[()] = "HexGrid".encode()
        with pytest.raises(IOError, match="Only square grids are"):
            _ = load(EDAX_FILE)
        with File(EDAX_FILE, mode="r+") as f:
            grid = f["Scan 1/EBSD/Header/Grid Type"]
            grid[()] = "SqrGrid".encode()

        s = load(EDAX_FILE)
        assert s.data.shape == (3, 3, 60, 60)
        assert_dictionary(s.axes_manager.as_dictionary(), AXES_MANAGER)

    def test_save_error(self):
        s = load(EDAX_FILE)
        with pytest.raises(OSError, match="(.*) is not a supported kikuchipy"):
            s.save(EDAX_FILE, add_scan=True)
