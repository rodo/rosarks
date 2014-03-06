from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def piwik_js():
    """Add a the piwik javascript code to template
    """
    try:
        return """
    <script type="text/javascript">
      var _paq = _paq || [];
      _paq.push(["trackPageView"]);
      _paq.push(["enableLinkTracking"]);
      
      (function() {
      var u=(("https:" == document.location.protocol) ? "https" :
      "http") + "://%s/";
      _paq.push(["setTrackerUrl", u+"piwik.php"]);
      _paq.push(["setSiteId", "%s"]);
      var d=document, g=d.createElement("script"),
      s=d.getElementsByTagName("script")[0]; g.type="text/javascript";
      g.defer=true; g.async=true; g.src=u+"piwik.js";
      s.parentNode.insertBefore(g,s);
      })();
    </script>
""" % (settings.PIWIK_SERVER, settings.PIWIK_ID)
    except:
        return ""
