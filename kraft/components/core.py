# SPDX-License-Identifier: BSD-3-Clause
#
# Authors: Alexander Jung <alexander.jung@neclab.eu>
#
# Copyright (c) 2020, NEC Europe Ltd., NEC Corporation. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from __future__ import absolute_import
from __future__ import unicode_literals

from kraft.components.repository import Repository
from kraft.components.types import RepositoryType


class Core(Repository):
    @classmethod
    def from_config(cls, ctx, config=None, save_cache=True):
        assert ctx is not None, "ctx is undefined"

        source = None
        version = None

        if 'source' in config:
            source = config['source']

        if 'version' in config:
            version = config['version']

        return super(Core, cls).from_unikraft_origin(
            name=None,
            source=source,
            version=version,
            repository_type=RepositoryType.CORE,
            save_cache=save_cache,
        )

    @classmethod
    def from_unikraft_origin(cls, source=None, version=None, save_cache=True):
        return super(Core, cls).from_unikraft_origin(
            name=None,
            source=source,
            version=version,
            repository_type=RepositoryType.CORE,
            save_cache=save_cache,
        )

    # One day we will need this
    # e.g.
    #    if core.compatible(UK_COMPAT_CORE_v0_4_0):
    #
    def compatible(self, version):
        return True
