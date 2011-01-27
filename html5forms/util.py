from django.utils.html import conditional_escape


def flatatt(attrs):
    """
    Convert a dictionary of attributes to a single string.
    The returned string will contain a leading space followed by key="value",
    XML-style pairs.  It is assumed that the keys do not need
    to be XML-escaped.
    If the passed dictionary is empty, then return an empty string.
    If the value passed is None writes only the attribute (eg. required)
    """
    ret_arr = []
    for k, v in attrs.items():

        if v is None:
            ret_arr.append(u' %s' % k)
        else:
            ret_arr.append(u' %s="%s"' % (k, conditional_escape(v)))
    return u''.join(ret_arr)


def render_datalist(name, datalist):
    ret_arr = [u'<datalist id="%s">' % name]
    for k, v in datalist:
        ret_arr.append(u"""<option label="%s" value="%s">"""
                % (conditional_escape(v), conditional_escape(k)))

    ret_arr.append(u'</datalist>')
    return u''.join(ret_arr)
