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
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITYs, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from __future__ import absolute_import
from __future__ import unicode_literals

import os

from kraft.components.executor import ExecutorDriverEnum
from kraft.components.repository import Repository
from kraft.components.repository import RepositoryManager
from kraft.components.types import RepositoryType
from kraft.constants import UK_CORE_PLAT_DIR


class Platform(Repository):
    _executor = None

    @property
    def executor(self):
        return self._executor

    @executor.setter
    def executor(self, executor):
        self._executor = executor

    @classmethod
    def from_config(cls,
                    ctx,
                    core=None,
                    plat=None,
                    config=None,
                    executor_base=None,
                    save_cache=True):
        assert ctx is not None, "ctx is undefined"

        if not core.is_downloaded:
            core.update()

        # Set the executor to the base in case we cannot later determine
        executor = executor_base
        executor_config = None
        platform = None

        if not isinstance(config, bool):
            if 'run' in config:
                executor_config = config['run']

            if 'source' in config:
                platform = super(Platform, cls).from_unikraft_origin(
                    source=config['source'],
                    repository_type=RepositoryType.PLAT,
                    save_cache=save_cache,
                )

        if platform is None:
            # Check if we have a cache hit for this platform name.   We do this
            # here because we are unsure of its source address, which can be
            # mis-interpretted as unikraft's core -- since we place the
            # platform INTO the unikraft core.
            cached_plat = ctx.cache.find_by_name(plat)
            if cached_plat is not None:
                platform = cached_plat
            else:
                platform = cls(
                    name=plat,
                    source=core.source,
                    version=core.version,
                    localdir=os.path.join(UK_CORE_PLAT_DIR % core.localdir, plat),
                    repository_type=RepositoryType.PLAT,
                    save_cache=save_cache,
                )

        # Determine executor driver
        for driver_name, member in ExecutorDriverEnum.__members__.items():
            if member.name == plat:
                executor = member.cls.from_config(
                    ctx=ctx,
                    config=executor_config,
                    executor_base=executor_base
                )
                break

        platform.executor = executor
        return platform

    @classmethod
    def from_unikraft_origin(cls, name, source=None, save_cache=True):
        return super(Platform, cls).from_unikraft_origin(
            name=name,
            source=source,
            repository_type=RepositoryType.PLAT,
            save_cache=save_cache,
        )


class Platforms(RepositoryManager):
    pass
