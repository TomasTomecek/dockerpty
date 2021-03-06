# dockerpty: non_interactive.feature.
#
# Copyright 2014 Chris Corbyn <chris@w3style.co.uk>
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


Feature: Attaching to a docker container non-interactively
  As a user I want to be able to attach to a process in a running docker
  container and view its output in my own terminal.


  Scenario: Capturing output
    Given I am using a TTY
    And I run "/usr/bin/tail -f /etc/issue" in a docker container
    When I start dockerpty
    Then I will see the output
      """
      Welcome to Buildroot
      """


  Scenario: Capturing errors
    Given I am using a TTY
    And I run "sh -c 'tail -f /etc/issue 1>&2'" in a docker container
    When I start dockerpty
    Then I will see the output
      """
      Welcome to Buildroot
      """


  Scenario: Ignoring input
    Given I am using a TTY
    And I run "/usr/bin/tail -f /etc/issue" in a docker container
    When I start dockerpty
    And I press ENTER
    Then I will see the output
      """
      Welcome to Buildroot
      """
    And The container will still be running


  Scenario: Running when the container is started
    Given I am using a TTY
    And I run "/bin/watch -n5 cat /etc/issue" in a docker container
    When I start the container
    And I start dockerpty
    Then I will see the output
      """
      Welcome to Buildroot
      """
