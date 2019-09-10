from jinja2 import Template

person = { "name": "Peter", "age": 34 }

tm = Template("My name is {{ per.name }} and I am {{ per.age }}")
msg = tm.render(per=person)

print(msg)