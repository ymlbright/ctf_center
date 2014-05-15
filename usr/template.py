from django import template
import datetime

def do_getPassed(parser,token):
	try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    return CurrentTimeNode(format_string[1:-1])

class CurrentTimeNode(template.Node):
	def __init__(self,format_string):
		self.format_string = format_string

	def render(self,context):
		now = datetime.datetime.now()
		return now.strftime(self.format_string)

