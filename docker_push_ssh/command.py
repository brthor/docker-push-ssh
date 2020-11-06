# Copyright 2018, Bryan Thornbury
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess


class Command(object):
    executable = None
    arguments = None

    def __init__(self, executable, arguments):
        """
        :type executable: str
        :type arguments: list[str]
        :param executable:
        :param arguments:
        :return:
        """

        self.executable = executable
        self.arguments = arguments

        self.environment_variables = dict()

    def environment(self, key, value):
        self.environment_variables[key] = value
        return self

    def environment_dict(self, env_dict):
        for key, value in env_dict.items():
            self.environment_variables[key] = value
        return self

    def execute(self, waitForExit=True):
        s_process_args = [self.executable]
        s_process_args.extend(self.arguments)

        s_process = subprocess.Popen(
            s_process_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.environment_variables)

        if waitForExit:
            out, err = s_process.communicate()
            exitcode = s_process.returncode
        else:
            out, err, exitcode = None, None, None

        # print out
        # print err

        return ProcessResult(self, out, err, exitcode, s_process.pid)


class ProcessResult(object):
    """
    :type process: Command
    :type s_process: subprocess.Popen
    :type stdout: str
    :type std
    """

    def __init__(self, process, stdout, stderr, exitcode, pid):
        self.process = process
        self.stdout = stdout
        self.stderr = stderr
        self.exitcode = exitcode
        self.pid = pid

    def failed(self):
        return self.exitcode != 0
