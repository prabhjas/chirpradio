# Copyright 2008 Google Inc.
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

"""Bootstrap for running a Django app under Google App Engine.

The site-specific code is all in other files: settings.py, urls.py,
models.py, views.py.  And in fact, only 'settings' is referenced here
directly -- everything else is controlled from there.

"""

# Standard Python imports.
import os
import sys
import logging

import appengine_django
from appengine_django import InstallAppengineHelperForDjango
if not hasattr(appengine_django, '_installed'):
  # this ensures that the setup code only gets called once.
  # i.e. if there is an exception in main.py then it will be reloaded 
  # even though other parts of the app are still in memory.
  # if this runs twice then mutiple instances of django might get loaded.
  InstallAppengineHelperForDjango()
  appengine_django._installed = True

from appengine_django import have_django_zip
from appengine_django import django_zip_path

# Google App Engine imports.
from google.appengine.ext.webapp import util

def main():
  # Ensure the Django zipfile is in the path if required.
  if have_django_zip and django_zip_path not in sys.path:
    sys.path.insert(1, django_zip_path)

  # Import the part of Django that we use here.
  import django.core.handlers.wsgi

  # Map the contents of the django-extras tree into the django
  # module's namespace.
  import django
  django.__path__.append('django-extras')

  # Pull in CHIRP's monkey-patching of Django
  from django import _monkey_patch

  # Create a Django application for WSGI.
  application = django.core.handlers.wsgi.WSGIHandler()

  # Run the WSGI CGI handler with that application.
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()