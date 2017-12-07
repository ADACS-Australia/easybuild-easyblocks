# #
# Copyright 2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# https://github.com/easybuilders/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
# #
"""
EasyBuild support for installing Intel Inspector, implemented as an easyblock

@author: Kenneth Hoste (Ghent University)
@author: Damian Alvarez (Forschungzentrum Juelich GmbH)
"""
import os
from distutils.version import LooseVersion

from easybuild.easyblocks.generic.intelbase import IntelBase, ACTIVATION_NAME_2012, LICENSE_FILE_NAME_2012


class EB_Inspector(IntelBase):
    """
    Support for installing Intel Inspector
    """

    def __init__(self, *args, **kwargs):
        """Easyblock constructor; define class variables."""
        super(EB_Inspector, self).__init__(*args, **kwargs)

        # recent versions of Inspector are installed to a subdirectory
        self.subdir = ''
        if LooseVersion(self.version) >= LooseVersion('2013_update7') and \
           LooseVersion(self.version) < LooseVersion('2017'):
            self.subdir = 'inspector_xe'
        elif LooseVersion(self.version) >= LooseVersion('2017'):
            self.subdir = 'inspector'

    def make_installdir(self):
        """Do not create installation directory, install script handles that already."""
        super(EB_Inspector, self).make_installdir(dontcreate=True)

    def install_step(self):
        """
        Actual installation
        - create silent cfg file
        - execute command
        """
        silent_cfg_names_map = None

        if LooseVersion(self.version) <= LooseVersion('2013_update6'):
            silent_cfg_names_map = {
                'activation_name': ACTIVATION_NAME_2012,
                'license_file_name': LICENSE_FILE_NAME_2012,
            }

        super(EB_Inspector, self).install_step(silent_cfg_names_map=silent_cfg_names_map)

    def make_module_req_guess(self):
        """Find reasonable paths for Inspector"""
        return _get_guesses_tools(self)

    def sanity_check_step(self):
        """Custom sanity check paths for Intel Inspector."""
        binaries = ['inspxe-cl', 'inspxe-feedback', 'inspxe-gui', 'inspxe-runmc', 'inspxe-runtc']
        custom_paths = _get_custom_paths_tools(self, binaries)
        super(EB_Inspector, self).sanity_check_step(custom_paths=custom_paths)
