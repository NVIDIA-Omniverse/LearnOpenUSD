# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""MyST directive for Kaltura video embeds."""

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class KalturaDirective(SphinxDirective):
    """MyST directive for embedding Kaltura videos."""
    
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    
    def run(self):
        """Process the kaltura directive."""
        if not self.arguments:
            return []
            
        video_id = self.arguments[0].strip()
        
        # Use the same HTML structure as the _nvfunc.py kaltura function
        kaltura_html = f'''<div class="video-container">
  <iframe
	src="https://cdnapisec.kaltura.com/p/2935771/embedPlaykitJs/uiconf_id/53712482?iframeembed=true&entry_id={video_id}"
	title="video"
	allowfullscreen
	webkitallowfullscreen
	mozAllowFullScreen
	allow="autoplay *; fullscreen *; encrypted-media *"
	frameborder="0">
  </iframe>
</div>'''
        
        raw_node = nodes.raw('', kaltura_html, format='html')
        return [raw_node]


def setup(app: Sphinx):
    """Sphinx extension setup function."""
    
    # Add the directives
    app.add_directive('kaltura', KalturaDirective)
    
    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    } 