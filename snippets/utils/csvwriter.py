import csv

from django.http import StreamingHttpResponse

import six


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def csv_streaming_response(filename, source):
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter=';')
    data = (
        writer.writerow([str(x).encode('cp1251', 'ignore') for x in row])
        for row in source
    )
    response = StreamingHttpResponse(data, content_type='text/csv')
    response['Content-Disposition'] = six.binary_type('attachment; filename="%s"' % filename)

    del pseudo_buffer
    return response


def csv_write(fileobj, source):
    writer = csv.writer(fileobj, delimiter=';')

    for row in source:
        writer.writerow([str(x).encode('cp1251', 'ignore') for x in row])
