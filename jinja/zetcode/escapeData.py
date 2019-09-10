from jinja2 import Template, escape

data = "<a>Today is a funny day</a>"

tm = Template("{{ data }}")
msg = tm.render(data=data)
print(msg)
print(escape(msg))