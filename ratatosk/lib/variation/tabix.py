# Copyright (c) 2013 Per Unneberg
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
import os
import luigi
import logging
import ratatosk.lib.files.external
from ratatosk.job import InputJobTask, JobTask, DefaultShellJobRunner

class TabixJobRunner(DefaultShellJobRunner):
    pass

class InputVcfFile(InputJobTask):
    _config_section = "tabix"
    _config_subsection = "InputVcfFile"
    parent_task = luigi.Parameter(default="ratatosk.lib.files.external.VcfFile")
    target_suffix = luigi.Parameter(default=".vcf")

class TabixJobTask(JobTask):
    _config_section = "tabix"
    executable = ""

    def job_runner(self):
        return TabixJobRunner()

    def exe(self):
        return self.sub_executable
    
    def main(self):
        return None

class TabixBgzipJobTask(TabixJobTask):
    _config_subsection = "bgzip"
    sub_executable = luigi.Parameter(default="bgzip")
    parent_task = luigi.Parameter(default="ratatosk.lib.variation.tabix.InputVcfFile")
    target_suffix = luigi.Parameter(default=".gz")
    source_suffix = luigi.Parameter(default="")

    def args(self):
        return [self.input()]

# Since this is such a common operation, add the task here
class TabixBgUnzipJobTask(TabixJobTask):
    _config_subsection = "bgunzip"
    sub_executable = luigi.Parameter(default="bgzip")
    parent_task = luigi.Parameter(default="ratatosk.lib.variation.tabix.InputVcfFile")
    target_suffix = luigi.Parameter(default=".vcf")
    source_suffix = luigi.Parameter(default=".vcf.gz")

    def opts(self):
        retval = list(self.options)
        if not "-d" in retval:
            retval += ["-d"]
        return retval

    def args(self):
        return [self.input()]


class TabixTabixJobTask(TabixJobTask):
    _config_subsection = "tabix"
    sub_executable = luigi.Parameter(default="tabix")
    parent_task = luigi.Parameter(default="ratatosk.lib.variation.tabix.TabixBgzipJobTask")
    target_suffix = luigi.Parameter(default=".gz.tbi")
    source_suffix = luigi.Parameter(default=".gz")

    def args(self):
        return [self.input()]
    
