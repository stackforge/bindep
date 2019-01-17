# Copyright (c) 2019 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Bootstrap with a manual bindep builder image so we don't wind up
# with the bindep source code in the final bindep builder image
FROM python:slim as builder

RUN apt-get update \
  && apt-get install -y git
COPY . /tmp/src
COPY docker/scripts/install-from-bindep /output/install-from-bindep
RUN pip install -e /tmp/src
RUN /tmp/src/docker/scripts/assemble

FROM python:slim

RUN apt-get update \
  && apt-get install -y git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
COPY docker/scripts/ /usr/local/bin
COPY --from=builder /output/ /output
RUN install-from-bindep
