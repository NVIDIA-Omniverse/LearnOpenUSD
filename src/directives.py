# Copyright (c) 2024, NVIDIA CORPORATION. All rights reserved.
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


class SurveyDirective(SphinxDirective):
    """MyST directive for embedding surveys."""
    
    has_content = False
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    
    def run(self):
        """Process the survey directive."""
        tag = self.arguments[0].strip() if self.arguments else ''
        tag = tag.replace(" ", "+")
        
        # Use the same HTML structure as the _nvfunc.py survey function
        survey_html = f'''<p>Your feedback is incredibly valuable to us as we continue to enhance our course content. If you have any thoughts on how we can improve or if you've encountered any issues, please take a moment to share your experience.</p>
<!-- Button for loading the survey-->
<p><button href="#" class="styled-button" id="openPopupButton"> Feedback Survey </button></p>
<p>
<script>
document.addEventListener('DOMContentLoaded', function () {{
    const openPopupButton = document.getElementById('openPopupButton');
    if (openPopupButton) {{
        openPopupButton.addEventListener('click', function (event) {{
            event.preventDefault();
            let pageTitle = document.title;
            const plusIndex = pageTitle.indexOf('Courseware');
            if (plusIndex !== -1) {{
                pageTitle = pageTitle.slice(0, plusIndex).trim();
            }}
            const hotjarUrl = new URL("https://surveys.hotjar.com/98510484-7ad7-4ddc-bfc4-1b7663827216");
            hotjarUrl.searchParams.append("utm_source", pageTitle);
            window.open(
                hotjarUrl.toString(),
                'popupWindow',
                'width=700,height=700,scrollbars=yes'
            );
        }});
    }}
}});
</script>
</p>'''
        
        raw_node = nodes.raw('', survey_html, format='html')
        return [raw_node]


class HtmlIncludeDirective(SphinxDirective):
    """MyST directive for including HTML content."""
    
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    
    def run(self):
        """Process the html_include directive."""
        if not self.arguments:
            return []
            
        url = self.arguments[0].strip()
        
        # Use the same HTML structure as the _nvfunc.py html_include function
        html_include_html = f'''<div w3-include-html="{url}"></div>
<script>
  function addHTML() {{
    var el, i, domEl, fileName, xmlHttp;

    /*Iterate all DOM*/
    el = document.getElementsByTagName("*");
    for (i = 0; i < el.length; i++) {{
      domEl = el[i];

      /*find the element having w3-include-html attribute*/
      fileName = domEl.getAttribute("w3-include-html");
      if (fileName) {{

        /*http request with attribute value as file name*/
        xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() {{
          if (this.readyState == 4) {{
            if (this.status == 200) {{
              domEl.innerHTML = this.responseText;
            }}
            if (this.status == 404) {{
              domEl.innerHTML = "Page not found.";
            }}

            /* Remove the attribute and invoke the function again*/
            domEl.removeAttribute("w3-include-html");
            addHTML();
          }}
        }}
        xmlHttp.open("GET", fileName, true);
        xmlHttp.send();

        /*function ends*/
        return;
      }}
    }}
  }}
  addHTML();
</script>'''
        
        raw_node = nodes.raw('', html_include_html, format='html')
        return [raw_node]


def setup(app: Sphinx):
    """Sphinx extension setup function."""
    
    # Add the directives
    app.add_directive('kaltura', KalturaDirective)
    # app.add_directive('survey', SurveyDirective)
    # app.add_directive('html-include', HtmlIncludeDirective)
    
    return {
        'version': '0.1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    } 