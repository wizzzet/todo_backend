#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.admin')

    import locale
    locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF8'))

    this_file_dir = os.path.dirname(os.path.abspath(__file__))

    sys.path.insert(0, this_file_dir)
    sys.path.insert(0, os.path.join(this_file_dir, 'project'))
    sys.path.insert(0, os.path.join(this_file_dir, 'apps'))

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
